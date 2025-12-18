from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    # 头像：允许保存图片 URL 或 base64 data URL（便于前端直接展示）
    avatar = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'users'

class WifiModel(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    signal_strength = models.FloatField()
    speed = models.FloatField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    rating = models.FloatField(default=0)
    review_count = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'wifi_models'

class DataPlan(models.Model):
    wifi_model = models.ForeignKey(WifiModel, related_name='data_plans', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = 'data_plans'

class Review(models.Model):
    wifi_model = models.ForeignKey(WifiModel, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    date = models.DateField(auto_now_add=True)
    is_anonymous = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'reviews'

class Favorite(models.Model):
    user = models.ForeignKey(User, related_name='favorites', on_delete=models.CASCADE)
    wifi_model = models.ForeignKey(WifiModel, related_name='favorited_by', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'favorites'
        unique_together = ('user', 'wifi_model')
