from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.db.models import Avg
from django.utils import timezone
from django.conf import settings
from django.http import FileResponse, Http404
import os
from .models import User, WifiModel, Review, Favorite
from .serializers import UserSerializer, UserProfileSerializer, WifiModelSerializer, ReviewSerializer, FavoriteSerializer
from .utils import process_and_save_avatar, delete_old_avatar

class WifiModelViewSet(viewsets.ModelViewSet):
    queryset = WifiModel.objects.all()
    serializer_class = WifiModelSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        # 默认只展示已通过的型号，避免未审核数据出现在公开列表
        return WifiModel.objects.filter(approval_status=WifiModel.APPROVAL_APPROVED)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]
    
    def perform_create(self, serializer):
        review = serializer.save()
        # 更新WiFi模型的评分和评论数
        wifi_model = review.wifi_model
        wifi_model.review_count = wifi_model.reviews.count()
        wifi_model.rating = wifi_model.reviews.aggregate(Avg('rating'))['rating__avg']
        wifi_model.save()

class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [AllowAny]

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # 为用户创建Token
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'message': '注册成功！',
                'token': token.key,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'date_joined': user.date_joined,
                    'avatar': user.avatar
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
        
        # 查找用户
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': '邮箱或密码错误'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # 验证密码
        user = authenticate(request, username=user.username, password=password)
        if user is not None:
            # 获取或创建Token
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'message': '登录成功！',
                'token': token.key,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'date_joined': user.date_joined,
                    'avatar': user.avatar
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({'message': '邮箱或密码错误'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET', 'PATCH', 'PUT'])
@permission_classes([IsAuthenticated])
def get_user_profile(request, user_id):
    """
    GET: 获取用户资料（含 avatar / date_joined）
    PATCH/PUT: 更新用户资料（当前仅支持 avatar）
    注意：用户只能查看和修改自己的资料
    """
    if request.user.id != user_id:
        return Response({'message': '无权访问其他用户的资料'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'message': '用户不存在'}, status=status.HTTP_404_NOT_FOUND)

    if request.method in ['PATCH', 'PUT']:
        avatar_file = request.FILES.get('avatar')
        clear_avatar = request.data.get('clear_avatar')
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        
        if clear_avatar == 'true' or clear_avatar is True:
            delete_old_avatar(user)
            user.avatar = None
            user.save(update_fields=['avatar'])
            serializer = UserProfileSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        if avatar_file:
            success, result = process_and_save_avatar(user, avatar_file)
            if not success:
                return Response({'message': result}, status=status.HTTP_400_BAD_REQUEST)
            
            delete_old_avatar(user)
            user.avatar = result
            user.save(update_fields=['avatar'])
            serializer = UserProfileSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        if username or email:
            if not password:
                return Response({'message': '请输入密码以验证身份'}, status=status.HTTP_400_BAD_REQUEST)
            
            verified_user = authenticate(request, username=user.username, password=password)
            if not verified_user:
                return Response({'message': '密码错误，无法修改个人信息'}, status=status.HTTP_401_UNAUTHORIZED)
            
            if username:
                user.username = username
            if email:
                user.email = email
            user.save(update_fields=['username', 'email'])
            serializer = UserProfileSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({'message': '请上传头像文件或指定要更新的字段'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = UserProfileSerializer(user)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_wifi_model_reviews(request, wifi_model_id):
    try:
        reviews = Review.objects.filter(wifi_model_id=wifi_model_id)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    except Exception:
        return Response({'error': '获取评价列表失败'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_favorites(request, user_id):
    # 验证用户只能查看自己的收藏
    if request.user.id != user_id:
        return Response({'message': '无权访问其他用户的收藏'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        favorites = Favorite.objects.filter(user_id=user_id)
        serializer = FavoriteSerializer(favorites, many=True)
        return Response(serializer.data)
    except Exception:
        return Response({'error': '获取收藏列表失败'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_reviews(request, user_id):
    # 验证用户只能查看自己的评价
    if request.user.id != user_id:
        return Response({'message': '无权访问其他用户的评价'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        reviews = Review.objects.filter(user_id=user_id)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    except Exception:
        return Response({'error': '获取评价列表失败'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_wifi_model(request):
    """
    普通用户提交新 WiFi 型号（默认进入待审核），同时可提交资费套餐：
    {
      "name": "...",
      "brand": "...",
      "model": "...",
      "signalStrength": 4.5,
      "speed": 4.8,
      "price": 299,
      "description": "...",
      "dataPlans": [{"name":"月包10GB","price":39}, ...]
    }
    兼容蛇形字段：signal_strength/signalStrength, data_plans/dataPlans
    注意：使用当前登录用户的ID，不再从请求中获取userId
    """
    # 使用当前认证的用户（IsAuthenticated装饰器已经确保用户已认证）
    user = request.user

    name = request.data.get('name')
    brand = request.data.get('brand')
    model = request.data.get('model')
    description = request.data.get('description', '')

    signal_strength = request.data.get('signal_strength', request.data.get('signalStrength'))
    speed = request.data.get('speed')
    price = request.data.get('price')

    if not name or not brand or not model:
        return Response({'message': '缺少 name/brand/model'}, status=status.HTTP_400_BAD_REQUEST)
    if signal_strength is None or speed is None or price is None:
        return Response({'message': '缺少 signalStrength/speed/price'}, status=status.HTTP_400_BAD_REQUEST)

    data_plans = request.data.get('data_plans', request.data.get('dataPlans', [])) or []
    if not isinstance(data_plans, list):
        return Response({'message': 'dataPlans 必须是数组'}, status=status.HTTP_400_BAD_REQUEST)

    wifi_model = WifiModel.objects.create(
        name=name,
        brand=brand,
        model=model,
        signal_strength=signal_strength,
        speed=speed,
        price=price,
        description=description,
        rating=0,
        review_count=0,
        approval_status=WifiModel.APPROVAL_PENDING,
        submitted_by=user,
        submitted_at=timezone.now(),
    )

    # 创建套餐
    for dp in data_plans:
        if not isinstance(dp, dict):
            continue
        dp_name = dp.get('name')
        dp_price = dp.get('price')
        if not dp_name or dp_price is None:
            continue
        from .models import DataPlan
        DataPlan.objects.create(wifi_model=wifi_model, name=dp_name, price=dp_price)

    serializer = WifiModelSerializer(wifi_model)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_wifi_model_submissions(request, user_id):
    """
    查看某用户提交的型号（含 pending/rejected/approved）
    注意：用户只能查看自己提交的型号
    """
    # 验证用户只能查看自己提交的型号
    if request.user.id != user_id:
        return Response({'message': '无权访问其他用户提交的型号'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        qs = WifiModel.objects.filter(submitted_by_id=user_id).order_by('-submitted_at', '-id')
        serializer = WifiModelSerializer(qs, many=True)
        return Response(serializer.data)
    except Exception:
        return Response({'error': '获取提交记录失败'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_review(request):
    """
    添加评价，使用当前登录用户：
    {
      "wifiModelId": 2,
      "rating": 5,
      "comment": "xxx",
      "isAnonymous": false
    }
    """
    # 使用当前认证的用户
    user = request.user
    wifi_model_id = request.data.get('wifiModelId')
    rating = request.data.get('rating')
    comment = request.data.get('comment', '')
    raw_is_anonymous = request.data.get('isAnonymous', request.data.get('is_anonymous', False))

    def _to_bool(v):
        if isinstance(v, bool):
            return v
        if v is None:
            return False
        if isinstance(v, (int, float)):
            return v != 0
        if isinstance(v, str):
            return v.strip().lower() in ['true', '1', 'yes', 'y', 'on']
        return bool(v)

    if not wifi_model_id:
        return Response({'message': '缺少 wifiModelId'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        wifi_model = WifiModel.objects.get(id=wifi_model_id)

        review = Review.objects.create(
            user=user,
            wifi_model=wifi_model,
            rating=rating,
            comment=comment,
            is_anonymous=_to_bool(raw_is_anonymous)
        )

        # 更新WiFi模型的评分和评论数
        wifi_model.review_count = wifi_model.reviews.count()
        wifi_model.rating = wifi_model.reviews.aggregate(Avg('rating'))['rating__avg']
        wifi_model.save()

        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except WifiModel.DoesNotExist:
        return Response({'message': 'WiFi模型不存在'}, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return Response({'error': '添加评价失败'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_favorite(request):
    if request.method == 'POST':
        # 使用当前认证的用户
        user = request.user
        wifi_model_id = request.data.get('wifiModelId')
        
        try:
            wifi_model = WifiModel.objects.get(id=wifi_model_id)
            
            favorite, created = Favorite.objects.get_or_create(user=user, wifi_model=wifi_model)
            if created:
                return Response({'message': '收藏成功！'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': '已经收藏过了！'}, status=status.HTTP_200_OK)
        except WifiModel.DoesNotExist:
            return Response({'message': 'WiFi模型不存在'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_favorite(request):
    if request.method == 'DELETE':
        # 使用当前认证的用户
        user = request.user
        wifi_model_id = request.data.get('wifiModelId')
        
        try:
            favorite = Favorite.objects.get(user=user, wifi_model_id=wifi_model_id)
            favorite.delete()
            return Response({'message': '取消收藏成功！'}, status=status.HTTP_200_OK)
        except Favorite.DoesNotExist:
            return Response({'message': '收藏不存在'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_avatar(request, user_id):
    """
    获取用户头像文件
    路径: /api/avatar/<user_id>/
    """
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise Http404('用户不存在')
    
    if not user.avatar:
        raise Http404('用户未设置头像')
    
    file_path = os.path.join(settings.MEDIA_ROOT, user.avatar)
    
    if not os.path.exists(file_path):
        raise Http404('头像文件不存在')
    
    try:
        return FileResponse(open(file_path, 'rb'))
    except Exception:
        raise Http404('无法读取头像文件')