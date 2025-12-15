from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.db.models import Avg
from .models import User, WifiModel, Review, Favorite
from .serializers import UserSerializer, WifiModelSerializer, ReviewSerializer, FavoriteSerializer

class WifiModelViewSet(viewsets.ModelViewSet):
    queryset = WifiModel.objects.all()
    serializer_class = WifiModelSerializer
    permission_classes = [AllowAny]

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
def register(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': '注册成功！'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
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
            return Response({
                'message': '登录成功！',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({'message': '邮箱或密码错误'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_wifi_model_reviews(request, wifi_model_id):
    try:
        reviews = Review.objects.filter(wifi_model_id=wifi_model_id)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_user_favorites(request, user_id):
    try:
        favorites = Favorite.objects.filter(user_id=user_id)
        serializer = FavoriteSerializer(favorites, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_user_reviews(request, user_id):
    try:
        reviews = Review.objects.filter(user_id=user_id)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
def add_favorite(request):
    if request.method == 'POST':
        user_id = request.data.get('userId')
        wifi_model_id = request.data.get('wifiModelId')
        
        try:
            user = User.objects.get(id=user_id)
            wifi_model = WifiModel.objects.get(id=wifi_model_id)
            
            favorite, created = Favorite.objects.get_or_create(user=user, wifi_model=wifi_model)
            if created:
                return Response({'message': '收藏成功！'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': '已经收藏过了！'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message': '用户不存在'}, status=status.HTTP_404_NOT_FOUND)
        except WifiModel.DoesNotExist:
            return Response({'message': 'WiFi模型不存在'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([AllowAny])
def remove_favorite(request):
    if request.method == 'DELETE':
        user_id = request.data.get('userId')
        wifi_model_id = request.data.get('wifiModelId')
        
        try:
            favorite = Favorite.objects.get(user_id=user_id, wifi_model_id=wifi_model_id)
            favorite.delete()
            return Response({'message': '取消收藏成功！'}, status=status.HTTP_200_OK)
        except Favorite.DoesNotExist:
            return Response({'message': '收藏不存在'}, status=status.HTTP_404_NOT_FOUND)