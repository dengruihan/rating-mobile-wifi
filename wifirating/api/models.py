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

    APPROVAL_PENDING = 'pending'
    APPROVAL_APPROVED = 'approved'
    APPROVAL_REJECTED = 'rejected'
    APPROVAL_CHOICES = [
        (APPROVAL_PENDING, '待审核'),
        (APPROVAL_APPROVED, '已通过'),
        (APPROVAL_REJECTED, '已驳回'),
    ]

    approval_status = models.CharField(
        max_length=20,
        choices=APPROVAL_CHOICES,
        default=APPROVAL_APPROVED
    )
    submitted_by = models.ForeignKey(
        User,
        related_name='submitted_wifi_models',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    submitted_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(
        User,
        related_name='approved_wifi_models',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(null=True, blank=True)
    
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
