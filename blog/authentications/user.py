from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import exceptions

from blog.models import User


class MyJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        """
        根据 Token 中的 user_id 查找用户
        validated_token: 已验证的 Token 字典，包含 'user_id'
        返回: User 实例 或 抛出异常（用户不存在）
        """
        try:
            user_id = validated_token.get('user_id')
            if not user_id:
                raise exceptions.AuthenticationFailed('用户不存在')

            # 用 id 字段查找用户（假设主键是 id）
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                raise exceptions.AuthenticationFailed('用户不存在')

            return user
        except Exception as e:
            raise exceptions.AuthenticationFailed(f'认证失败: {str(e)}')
