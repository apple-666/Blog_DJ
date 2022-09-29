from django.db import models
from django.utils import timezone

# Create your models here.
from users.models import User


class ArticleCategory(models.Model):
    title = models.CharField(max_length=200, blank=True)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'tb_category'
        verbose_name = '类别管理'
        verbose_name_plural = verbose_name


class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='article/%Y%m%d/', blank=True)
    category = models.ForeignKey(
        ArticleCategory,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='article'
    )
    tags = models.CharField(max_length=30, blank=True)
    title = models.CharField(max_length=200, null=False, blank=False)
    sumary = models.CharField(max_length=400, null=False, blank=False)
    content = models.TextField()
    total_views = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(default=timezone.now())
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        # 按created的倒序 排列
        ordering = ('-created',)
        db_table = 'tb_article'
        verbose_name = '文章管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
