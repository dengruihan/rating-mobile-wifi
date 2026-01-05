import os
import hashlib
import secrets
import re
from django.conf import settings
from PIL import Image
import io
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
MAX_FILE_SIZE = 800 * 1024  # 800KB
MAX_IMAGE_DIMENSION = 1024  # 最大尺寸限制


def generate_encrypted_filename(original_filename):
    """
    生成加密的文件名
    使用SHA256哈希算法对原始文件名进行加密，并添加随机后缀
    """
    ext = os.path.splitext(original_filename)[1].lower()
    if not ext:
        ext = '.jpg'
    
    timestamp = str(int(secrets.token_hex(8), 16))
    hash_obj = hashlib.sha256((original_filename + timestamp).encode('utf-8'))
    encrypted_name = hash_obj.hexdigest()[:32]
    
    return f'{encrypted_name}{ext}'


def validate_image_file(file):
    """
    验证上传的图片文件
    返回: (is_valid, error_message)
    """
    if not file:
        return False, '未选择文件'
    
    if file.size > MAX_FILE_SIZE:
        return False, f'文件过大，请选择小于 {MAX_FILE_SIZE // 1024}KB 的图片'
    
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        return False, f'不支持的文件类型，请选择 {", ".join([t.split("/")[1].upper() for t in ALLOWED_IMAGE_TYPES])} 格式的图片'
    
    try:
        img = Image.open(file)
        img.verify()
        file.seek(0)
        
        width, height = img.size
        if width > MAX_IMAGE_DIMENSION or height > MAX_IMAGE_DIMENSION:
            return False, f'图片尺寸过大，最大支持 {MAX_IMAGE_DIMENSION}x{MAX_IMAGE_DIMENSION}'
        
    except Exception:
        return False, '文件不是有效的图片'
    
    return True, None


def process_and_save_avatar(user, uploaded_file):
    """
    处理并保存头像文件
    返回: (success, avatar_path_or_error_message)
    """
    is_valid, error_msg = validate_image_file(uploaded_file)
    if not is_valid:
        return False, error_msg
    
    encrypted_filename = generate_encrypted_filename(uploaded_file.name)
    
    user_avatar_dir = os.path.join(settings.MEDIA_ROOT, 'avatars', str(user.id))
    os.makedirs(user_avatar_dir, exist_ok=True)
    
    avatar_path = os.path.join(user_avatar_dir, encrypted_filename)
    
    try:
        img = Image.open(uploaded_file)
        
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        
        img.save(avatar_path, 'JPEG', quality=85, optimize=True)
        
        relative_path = os.path.join('avatars', str(user.id), encrypted_filename)
        return True, relative_path
        
    except Exception as e:
        if os.path.exists(avatar_path):
            os.remove(avatar_path)
        return False, f'保存头像失败: {str(e)}'


def delete_old_avatar(user):
    """
    删除用户的旧头像文件
    """
    if not user.avatar:
        return
    
    old_avatar_path = os.path.join(settings.MEDIA_ROOT, user.avatar)
    
    try:
        if os.path.exists(old_avatar_path):
            os.remove(old_avatar_path)
            
            user_avatar_dir = os.path.dirname(old_avatar_path)
            try:
                if not os.listdir(user_avatar_dir):
                    os.rmdir(user_avatar_dir)
                    
                    avatars_dir = os.path.dirname(user_avatar_dir)
                    if not os.listdir(avatars_dir):
                        os.rmdir(avatars_dir)
            except Exception:
                pass
    except Exception:
        pass


def cleanup_unused_avatars():
    """
    清理未使用的头像文件（数据库中不存在的文件）
    """
    from .models import User
    
    avatars_dir = os.path.join(settings.MEDIA_ROOT, 'avatars')
    
    if not os.path.exists(avatars_dir):
        return
    
    db_avatar_paths = set()
    for user in User.objects.exclude(avatar__isnull=True).exclude(avatar=''):
        if user.avatar:
            db_avatar_paths.add(os.path.join(settings.MEDIA_ROOT, user.avatar))
    
    for user_id_dir in os.listdir(avatars_dir):
        user_dir = os.path.join(avatars_dir, user_id_dir)
        
        if not os.path.isdir(user_dir):
            continue
            
        for filename in os.listdir(user_dir):
            file_path = os.path.join(user_dir, filename)
            
            if file_path not in db_avatar_paths:
                try:
                    os.remove(file_path)
                except Exception:
                    pass
        
        try:
            if not os.listdir(user_dir):
                os.rmdir(user_dir)
        except Exception:
            pass


def validate_password_strength(password):
    """
    验证密码强度
    要求：
    - 长度至少8位
    - 包含大小写字母、数字和特殊符号中的至少三种
    
    返回: (is_valid, error_message, strength_level)
    strength_level: 0-弱, 1-中, 2-强
    """
    if len(password) < 8:
        return False, '密码长度至少需要8位', 0
    
    has_upper = bool(re.search(r'[A-Z]', password))
    has_lower = bool(re.search(r'[a-z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
    
    criteria_count = sum([has_upper, has_lower, has_digit, has_special])
    
    if criteria_count < 3:
        return False, '密码需要包含大小写字母、数字和特殊符号中的至少三种', 0
    
    if criteria_count == 3:
        return True, '密码强度中等', 1
    
    return True, '密码强度强', 2


def generate_verification_code():
    """
    生成6位数字验证码
    """
    return ''.join([str(secrets.randbelow(10)) for _ in range(6)])


def send_verification_email(user, code, purpose='password_change'):
    """
    发送验证码邮件
    
    参数:
        user: 用户对象
        code: 验证码
        purpose: 验证码用途（password_change等）
    
    返回: (success, error_message)
    """
    try:
        subject = 'WiFi评分系统 - 验证码'
        
        purpose_text = {
            'password_change': '修改密码'
        }.get(purpose, '验证')
        
        message = f'''
尊敬的 {user.username}：

您好！

您正在进行{purpose_text}操作，验证码为：{code}

验证码有效期为15分钟，请尽快完成操作。

如果这不是您的操作，请忽略此邮件。

此致
WiFi评分系统团队
'''
        
        from_email = settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else None
        
        send_mail(
            subject,
            message,
            from_email,
            [user.email],
            fail_silently=False
        )
        
        logger.info(f'验证码邮件已发送至 {user.email}，用途：{purpose}')
        return True, None
        
    except Exception as e:
        logger.error(f'发送验证码邮件失败: {str(e)}')
        return False, f'发送验证码邮件失败: {str(e)}'


def check_verification_code_limit(user, purpose='password_change'):
    """
    检查用户在1小时内发送验证码的次数限制
    
    参数:
        user: 用户对象
        purpose: 验证码用途
    
    返回: (can_send, remaining_attempts, error_message)
    """
    from .models import VerificationCode
    
    one_hour_ago = timezone.now() - timedelta(hours=1)
    
    recent_codes = VerificationCode.objects.filter(
        user=user,
        purpose=purpose,
        created_at__gte=one_hour_ago
    ).count()
    
    MAX_ATTEMPTS = 5
    
    if recent_codes >= MAX_ATTEMPTS:
        return False, 0, f'您在1小时内已发送{MAX_ATTEMPTS}次验证码，请稍后再试'
    
    remaining_attempts = MAX_ATTEMPTS - recent_codes
    return True, remaining_attempts, None


def create_verification_code(user, email, purpose='password_change'):
    """
    创建验证码记录
    
    参数:
        user: 用户对象
        email: 邮箱地址
        purpose: 验证码用途
    
    返回: (verification_code, error_message)
    """
    from .models import VerificationCode
    
    code = generate_verification_code()
    expires_at = timezone.now() + timedelta(minutes=15)
    
    VerificationCode.objects.create(
        user=user,
        code=code,
        email=email,
        expires_at=expires_at,
        purpose=purpose
    )
    
    return code, None


def verify_code(user, code, purpose='password_change'):
    """
    验证验证码
    
    参数:
        user: 用户对象
        code: 用户输入的验证码
        purpose: 验证码用途
    
    返回: (is_valid, error_message)
    """
    from .models import VerificationCode
    
    try:
        verification = VerificationCode.objects.filter(
            user=user,
            code=code,
            purpose=purpose,
            is_used=False
        ).latest('created_at')
        
        if timezone.now() > verification.expires_at:
            return False, '验证码已过期，请重新获取'
        
        verification.is_used = True
        verification.save()
        
        return True, None
        
    except VerificationCode.DoesNotExist:
        return False, '验证码错误，请重新输入'
