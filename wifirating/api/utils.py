import os
import hashlib
import secrets
from django.conf import settings
from PIL import Image
import io

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
