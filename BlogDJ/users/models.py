from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    mobile = models.CharField(max_length=20, unique=True, blank=True)
    # 头像
    avatar = models.ImageField(upload_to='avatar/%Y%m%d/', blank=True)

    user_desc = models.TextField(max_length=500, blank=True)

    USERNAME_FIELD = 'mobile'

    REQUIRED_FIELDS = ['username', 'email']

    class Meta:
        db_table = 'tb_user'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name  # ??peng1.1

    def __str__(self):  # 一mobile作为名字输出
        return self.mobile
