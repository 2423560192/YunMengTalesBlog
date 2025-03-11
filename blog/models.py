from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.hashers import make_password, check_password
from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils import timezone


# 用户表（扩展 Django 自带 User 模型）
class User(models.Model):
    username = models.CharField(max_length=50, unique=True, verbose_name='用户名')
    password = models.CharField(max_length=128, verbose_name='密码')  # 存储加密后的密码
    email = models.EmailField(unique=True, blank=True, null=True, verbose_name='邮箱')
    nickname = models.CharField(max_length=50, blank=True, null=True, verbose_name='昵称')
    avatar = models.URLField(blank=True, null=True, verbose_name='头像 URL')
    bio = models.TextField(max_length=500, blank=True, null=True, verbose_name='简介')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='注册时间')
    is_active = models.BooleanField(default=True, verbose_name='是否激活')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
        indexes = [
            models.Index(fields=['username'], name='idx_username'),  # 加快用户名查询
        ]

    def __str__(self):
        return self.username

    @property
    def is_authenticated(self):
        return True

    def set_password(self, raw_password):
        """设置密码（加密存储）"""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """验证密码是否正确"""
        return check_password(raw_password, self.password)


# 分类表
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='分类名称')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'

    def __str__(self):
        return self.name


# 标签表
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='标签名称')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'

    def __str__(self):
        return self.name


# 文章表
class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='内容')  # Markdown 格式
    cover = models.URLField(blank=True, null=True, verbose_name='封面图片 URL')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='分类')
    tags = models.ManyToManyField(Tag, through='PostTag', blank=True, verbose_name='标签')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_published = models.BooleanField(default=True, verbose_name='是否发布')

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'
        indexes = [
            models.Index(fields=['created_at'], name='idx_created_at'),  # 按时间排序
            models.Index(fields=['title'], name='idx_title'),  # 搜索优化
        ]

    def __str__(self):
        return self.title


class PostTag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('post', 'tag')


# 评论表
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='文章')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    content = models.TextField(max_length=1000, verbose_name='评论内容')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name='父评论')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'
        indexes = [
            models.Index(fields=['post', 'created_at'], name='idx_post_created'),  # 按文章和时间查询
        ]

    def __str__(self):
        return f"{self.user.username} on {self.post.title}"


# 点赞表
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='文章')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='点赞时间')

    class Meta:
        verbose_name = '点赞'
        verbose_name_plural = '点赞'
        unique_together = ('post', 'user')  # 一个用户只能点赞一次
        indexes = [
            models.Index(fields=['post', 'user'], name='idx_post_user'),
        ]

    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"


# 收藏表
class Bookmark(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='文章')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='收藏时间')

    class Meta:
        verbose_name = '收藏'
        verbose_name_plural = '收藏'
        unique_together = ('post', 'user')  # 一个用户只能收藏一次
        indexes = [
            models.Index(fields=['user', 'created_at'], name='idx_user_created'),  # 个人中心查询
        ]

    def __str__(self):
        return f"{self.user.username} bookmarks {self.post.title}"
