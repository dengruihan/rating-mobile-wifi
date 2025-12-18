from rest_framework import serializers
from .models import User, WifiModel, DataPlan, Review, Favorite
from django.contrib.auth.password_validation import validate_password

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined', 'avatar']

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        validators=[validate_password],
        min_length=6,  # 设置最小密码长度
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
    
    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class DataPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataPlan
        fields = ['name', 'price']

class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')
    wifi_model_name = serializers.ReadOnlyField(source='wifi_model.name')
    user_avatar = serializers.ReadOnlyField(source='user.avatar')
    display_name = serializers.SerializerMethodField()
    display_avatar = serializers.SerializerMethodField()
    
    class Meta:
        model = Review
        fields = [
            'id',
            'wifi_model_id',
            'wifi_model_name',
            'user_id',
            'user_name',
            'user_avatar',
            'is_anonymous',
            'display_name',
            'display_avatar',
            'rating',
            'comment',
            'date',
        ]

    def get_display_name(self, obj):
        return '匿名' if getattr(obj, 'is_anonymous', False) else (obj.user.username if obj.user else '匿名')

    def get_display_avatar(self, obj):
        # 匿名时不暴露真实头像
        return None if getattr(obj, 'is_anonymous', False) else getattr(obj.user, 'avatar', None)

class WifiModelSerializer(serializers.ModelSerializer):
    data_plans = DataPlanSerializer(many=True, read_only=True)
    
    class Meta:
        model = WifiModel
        fields = [
            'id',
            'name',
            'brand',
            'model',
            'signal_strength',
            'speed',
            'price',
            'description',
            'rating',
            'review_count',
            'data_plans',
            'approval_status',
            'submitted_by',
            'submitted_at',
            'approved_by',
            'approved_at',
            'rejection_reason',
        ]

class FavoriteSerializer(serializers.ModelSerializer):
    wifi_model = WifiModelSerializer(read_only=True)
    wifi_model_id = serializers.PrimaryKeyRelatedField(queryset=WifiModel.objects.all(), write_only=True, source='wifi_model')
    
    class Meta:
        model = Favorite
        fields = ['id', 'user_id', 'wifi_model', 'wifi_model_id']
