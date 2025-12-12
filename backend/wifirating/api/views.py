from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import WifiModel, Favorite, Review, User
from django.db.models import Avg

# 获取所有WiFi模型
@csrf_exempt
def get_wifi_models(request):
    if request.method == 'GET':
        wifi_models = WifiModel.objects.all()
        data = []
        for model in wifi_models:
            data.append({
                'id': model.id,
                'name': model.name,
                'brand': model.brand,
                'model': model.model,
                'signalStrength': model.signalStrength,
                'speed': model.speed,
                'price': model.price,
                'description': model.description,
                'rating': model.rating,
                'reviewCount': model.reviewCount
            })
        return JsonResponse(data, safe=False)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

# 获取单个WiFi模型详情
@csrf_exempt
def get_wifi_model_detail(request, model_id):
    if request.method == 'GET':
        try:
            model = WifiModel.objects.get(id=model_id)
            data = {
                'id': model.id,
                'name': model.name,
                'brand': model.brand,
                'model': model.model,
                'signalStrength': model.signalStrength,
                'speed': model.speed,
                'price': model.price,
                'description': model.description,
                'rating': model.rating,
                'reviewCount': model.reviewCount
            }
            return JsonResponse(data)
        except WifiModel.DoesNotExist:
            return JsonResponse({'error': 'WiFi model not found'}, status=404)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

# 切换收藏状态
@csrf_exempt
def toggle_favorite(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('userId')
            wifi_model_id = data.get('wifiModelId')
            
            if not user_id or not wifi_model_id:
                return JsonResponse({'error': 'Missing user_id or wifi_model_id'}, status=400)
            
            user = User.objects.get(id=user_id)
            wifi_model = WifiModel.objects.get(id=wifi_model_id)
            
            favorite, created = Favorite.objects.get_or_create(
                userId=user,
                wifiModelId=wifi_model
            )
            
            return JsonResponse({'status': 'added', 'id': favorite.id})
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except WifiModel.DoesNotExist:
            return JsonResponse({'error': 'WiFi model not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    elif request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            user_id = data.get('userId')
            wifi_model_id = data.get('wifiModelId')
            
            if not user_id or not wifi_model_id:
                return JsonResponse({'error': 'Missing user_id or wifi_model_id'}, status=400)
            
            favorite = Favorite.objects.get(
                userId_id=user_id,
                wifiModelId_id=wifi_model_id
            )
            favorite.delete()
            
            return JsonResponse({'status': 'removed'})
        except Favorite.DoesNotExist:
            return JsonResponse({'error': 'Favorite not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

# 获取用户收藏
@csrf_exempt
def get_user_favorites(request, user_id):
    if request.method == 'GET':
        try:
            favorites = Favorite.objects.filter(userId_id=user_id)
            data = []
            for favorite in favorites:
                model = favorite.wifiModelId
                data.append({
                    'id': model.id,
                    'name': model.name,
                    'brand': model.brand,
                    'model': model.model,
                    'signalStrength': model.signalStrength,
                    'speed': model.speed,
                    'price': model.price,
                    'rating': model.rating,
                    'reviewCount': model.reviewCount
                })
            return JsonResponse(data, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

# 添加评价
@csrf_exempt
def add_review(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('userId')
            model_id = data.get('wifiModelId')
            rating = data.get('rating')
            comment = data.get('comment')
            
            if not user_id or not model_id or not rating:
                return JsonResponse({'error': 'Missing required fields'}, status=400)
            
            user = User.objects.get(id=user_id)
            wifi_model = WifiModel.objects.get(id=model_id)
            
            review = Review.objects.create(
                userId=user,
                wifiModelId=wifi_model,
                rating=rating,
                comment=comment
            )
            
            # 更新WiFi模型的平均评分和评价数量
            avg_rating = Review.objects.filter(wifiModelId=wifi_model).aggregate(Avg('rating'))['rating__avg']
            review_count = Review.objects.filter(wifiModelId=wifi_model).count()
            
            wifi_model.rating = avg_rating
            wifi_model.reviewCount = review_count
            wifi_model.save()
            
            return JsonResponse({
                'id': review.id,
                'userId': user_id,
                'wifiModelId': model_id,
                'rating': rating,
                'comment': comment,
                'createdAt': review.createdAt
            })
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except WifiModel.DoesNotExist:
            return JsonResponse({'error': 'WiFi model not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

# 获取模型评价
@csrf_exempt
def get_model_reviews(request, model_id):
    if request.method == 'GET':
        try:
            reviews = Review.objects.filter(wifiModelId_id=model_id)
            data = []
            for review in reviews:
                data.append({
                    'id': review.id,
                    'userId': review.userId_id,
                    'userName': review.userId.username,
                    'wifiModelId': review.wifiModelId_id,
                    'rating': review.rating,
                    'comment': review.comment,
                    'createdAt': review.createdAt
                })
            return JsonResponse(data, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

# 获取用户评价
@csrf_exempt
def get_user_reviews(request, user_id):
    if request.method == 'GET':
        try:
            reviews = Review.objects.filter(userId_id=user_id)
            data = []
            for review in reviews:
                model = review.wifiModelId
                data.append({
                    'id': review.id,
                    'wifiModelId': model.id,
                    'wifiModelName': model.name,
                    'rating': review.rating,
                    'comment': review.comment,
                    'createdAt': review.createdAt
                })
            return JsonResponse(data, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

# 用户登录
@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            
            if not email or not password:
                return JsonResponse({'message': '邮箱和密码不能为空'}, status=400)
            
            try:
                user = User.objects.get(email=email, password=password)
                return JsonResponse({
                    'message': '登录成功',
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email
                    }
                })
            except User.DoesNotExist:
                return JsonResponse({'message': '邮箱或密码错误'}, status=401)
                
        except Exception as e:
            return JsonResponse({'message': '登录失败', 'error': str(e)}, status=500)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

# 用户注册
@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            
            if not username or not email or not password:
                return JsonResponse({'message': '用户名、邮箱和密码不能为空'}, status=400)
            
            # 检查邮箱是否已存在
            if User.objects.filter(email=email).exists():
                return JsonResponse({'message': '邮箱已被注册'}, status=400)
            
            # 检查用户名是否已存在
            if User.objects.filter(username=username).exists():
                return JsonResponse({'message': '用户名已被使用'}, status=400)
            
            # 创建新用户
            user = User.objects.create(
                username=username,
                email=email,
                password=password
            )
            
            return JsonResponse({
                'message': '注册成功',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            })
            
        except Exception as e:
            return JsonResponse({'message': '注册失败', 'error': str(e)}, status=500)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

