from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import bcrypt

# 用户管理器
class UserManager(BaseUserManager):
    def create_user(self, username, email, password):
        if not username:
            raise ValueError('用户必须有用户名')
        if not email:
            raise ValueError('用户必须有邮箱')
        if not password:
            raise ValueError('用户必须有密码')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )

        # 使用bcrypt进行密码哈希
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user.password = hashed_password
        user.save(using=self._db)
        return user

# 用户模型
class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    registration_date = models.DateField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'User'

# WiFi型号模型
class WifiModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    signalStrength = models.FloatField()
    speed = models.FloatField()
    price = models.FloatField()
    description = models.TextField(blank=True, null=True)
    rating = models.FloatField(default=0)
    reviewCount = models.IntegerField(default=0)

    class Meta:
        db_table = 'WifiModel'

# 数据套餐模型
class DataPlan(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.FloatField()
    wifiModelId = models.ForeignKey(WifiModel, on_delete=models.CASCADE, db_column='wifiModelId')

    class Meta:
        db_table = 'DataPlan'

# 评价模型
class Review(models.Model):
    id = models.AutoField(primary_key=True)
    wifiModelId = models.ForeignKey(WifiModel, on_delete=models.CASCADE, db_column='wifiModelId')
    userId = models.ForeignKey(User, on_delete=models.CASCADE, db_column='userId')
    userName = models.CharField(max_length=100)
    rating = models.FloatField()
    comment = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'Review'

# 收藏模型
class Favorite(models.Model):
    id = models.AutoField(primary_key=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE, db_column='userId')
    wifiModelId = models.ForeignKey(WifiModel, on_delete=models.CASCADE, db_column='wifiModelId')

    class Meta:
        db_table = 'Favorite'
        unique_together = ('userId', 'wifiModelId')
