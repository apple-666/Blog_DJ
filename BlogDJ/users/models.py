from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    mobile = models.CharField(max_length=20, unique=True, blank=True)
    # 头像
    avatar = models.ImageField(upload_to='avatar/%Y%m%d/', blank=True)

    user_desc = models.TextField(max_length=500, blank=True)

    USERNAME_FIELD = 'mobile'

    # 创建超级管理员必要的字段
    REQUIRED_FIELDS = ['username', 'email']
    # 14467279371 fpp123456

    class Meta:  # 数据的处理
        db_table = 'tb_user'  # 设置表明
        verbose_name = '用户信息'  # 别名 (在admin后台中显示用)
        verbose_name_plural = verbose_name  # 别名的复数形式 ()

    def __str__(self):  # 一mobile作为名字输出 （在admin后台中国显示用）
        return self.mobile
