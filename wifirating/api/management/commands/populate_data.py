from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.db.models import Avg
from api.models import User, WifiModel, DataPlan, Review, Favorite
import datetime

class Command(BaseCommand):
    help = 'Populate the database with test data'

    def handle(self, *args, **kwargs):
        # Clear existing data
        self.stdout.write('Clearing existing data...')
        Favorite.objects.all().delete()
        Review.objects.all().delete()
        DataPlan.objects.all().delete()
        WifiModel.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        # Create users
        self.stdout.write('Creating users...')
        users_data = [
            {'username': '张三', 'email': 'zhangsan@example.com', 'password': 'password123'},
            {'username': '李四', 'email': 'lisi@example.com', 'password': 'password123'},
            {'username': '王五', 'email': 'wangwu@example.com', 'password': 'password123'},
            {'username': '赵六', 'email': 'zhaoliu@example.com', 'password': 'password123'},
            {'username': '孙七', 'email': 'sunqi@example.com', 'password': 'password123'},
        ]

        users = []
        for user_data in users_data:
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                password=make_password(user_data['password'])
            )
            user.save()
            users.append(user)

        # Create WiFi models and data plans
        self.stdout.write('Creating WiFi models and data plans...')
        wifi_models_data = [
            {
                'name': '华为随行WiFi 3',
                'brand': '华为',
                'model': 'E5576-855',
                'signal_strength': 4.5,
                'speed': 4.8,
                'price': 299,
                'description': '华为随行WiFi 3支持4G网络，最多可连接16台设备，续航时间长达8小时，适合旅行和办公使用。',
                'data_plans': [
                    {'name': '月包10GB', 'price': 39},
                    {'name': '月包20GB', 'price': 69},
                    {'name': '月包50GB', 'price': 129}
                ]
            },
            {
                'name': '小米移动WiFi',
                'brand': '小米',
                'model': 'R1CL',
                'signal_strength': 4.2,
                'speed': 4.5,
                'price': 199,
                'description': '小米移动WiFi采用简洁设计，支持4G网络，最多可连接10台设备，续航时间6小时，性价比高。',
                'data_plans': [
                    {'name': '月包5GB', 'price': 29},
                    {'name': '月包15GB', 'price': 59},
                    {'name': '月包30GB', 'price': 99}
                ]
            },
            {
                'name': '腾讯随身WiFi',
                'brand': '腾讯',
                'model': 'Tencent WiFi',
                'signal_strength': 3.8,
                'speed': 4.0,
                'price': 129,
                'description': '腾讯随身WiFi体积小巧，便于携带，支持4G网络，最多可连接8台设备，适合日常使用。',
                'data_plans': [
                    {'name': '月包3GB', 'price': 19},
                    {'name': '月包10GB', 'price': 49},
                    {'name': '月包20GB', 'price': 79}
                ]
            },
            {
                'name': '中兴MF920U',
                'brand': '中兴',
                'model': 'MF920U',
                'signal_strength': 4.6,
                'speed': 4.7,
                'price': 349,
                'description': '中兴MF920U支持4G+网络，最多可连接15台设备，续航时间长达10小时，信号稳定。',
                'data_plans': [
                    {'name': '月包15GB', 'price': 49},
                    {'name': '月包30GB', 'price': 89},
                    {'name': '月包60GB', 'price': 149}
                ]
            },
            {
                'name': 'TP-Link M7350',
                'brand': 'TP-Link',
                'model': 'M7350',
                'signal_strength': 4.3,
                'speed': 4.4,
                'price': 249,
                'description': 'TP-Link M7350支持4G网络，最多可连接10台设备，续航时间8小时，操作简单。',
                'data_plans': [
                    {'name': '月包8GB', 'price': 35},
                    {'name': '月包20GB', 'price': 65},
                    {'name': '月包40GB', 'price': 115}
                ]
            }
        ]

        wifi_models = []
        for wifi_data in wifi_models_data:
            wifi_model = WifiModel(
                name=wifi_data['name'],
                brand=wifi_data['brand'],
                model=wifi_data['model'],
                signal_strength=wifi_data['signal_strength'],
                speed=wifi_data['speed'],
                price=wifi_data['price'],
                description=wifi_data['description'],
                rating=0.0,
                review_count=0
            )
            wifi_model.save()
            wifi_models.append(wifi_model)

            # Create data plans for this wifi model
            for dp_data in wifi_data['data_plans']:
                data_plan = DataPlan(
                    wifi_model=wifi_model,
                    name=dp_data['name'],
                    price=dp_data['price']
                )
                data_plan.save()

        # Create reviews
        self.stdout.write('Creating reviews...')
        reviews_data = [
            {'wifi_model_index': 0, 'user_index': 0, 'rating': 5, 'comment': '信号非常稳定，在山区也能正常使用，续航时间很长，非常满意！', 'date': '2024-01-15'},
            {'wifi_model_index': 0, 'user_index': 1, 'rating': 4, 'comment': '速度很快，连接稳定，就是价格稍微有点贵。', 'date': '2024-01-10'},
            {'wifi_model_index': 1, 'user_index': 2, 'rating': 4, 'comment': '性价比很高，信号不错，适合日常使用。', 'date': '2024-01-05'},
            {'wifi_model_index': 2, 'user_index': 3, 'rating': 3, 'comment': '信号一般，在信号弱的地方会断连，价格便宜但体验一般。', 'date': '2024-01-01'},
            {'wifi_model_index': 3, 'user_index': 4, 'rating': 5, 'comment': '信号超级稳定，速度也很快，续航时间长，强烈推荐！', 'date': '2023-12-28'},
            {'wifi_model_index': 4, 'user_index': 0, 'rating': 4, 'comment': '操作简单，信号稳定，价格合理。', 'date': '2023-12-25'},
            {'wifi_model_index': 1, 'user_index': 4, 'rating': 5, 'comment': '非常好用，连接速度快，信号强。', 'date': '2023-12-20'},
        ]

        for review_data in reviews_data:
            review = Review(
                wifi_model=wifi_models[review_data['wifi_model_index']],
                user=users[review_data['user_index']],
                rating=review_data['rating'],
                comment=review_data['comment'],
                date=datetime.datetime.strptime(review_data['date'], '%Y-%m-%d').date()
            )
            review.save()

            # Update wifi model rating and review count
            wifi_model = review.wifi_model
            wifi_model.review_count = wifi_model.reviews.count()
            wifi_model.rating = wifi_model.reviews.aggregate(Avg('rating'))['rating__avg']
            wifi_model.save()

        # Create favorites
        self.stdout.write('Creating favorites...')
        favorites_data = [
            {'user_index': 0, 'wifi_model_index': 0},
            {'user_index': 0, 'wifi_model_index': 3},
            {'user_index': 1, 'wifi_model_index': 1},
            {'user_index': 2, 'wifi_model_index': 2},
            {'user_index': 3, 'wifi_model_index': 4},
            {'user_index': 4, 'wifi_model_index': 3},
        ]

        for fav_data in favorites_data:
            favorite = Favorite(
                user=users[fav_data['user_index']],
                wifi_model=wifi_models[fav_data['wifi_model_index']]
            )
            favorite.save()

        self.stdout.write(self.style.SUCCESS('Test data populated successfully!'))