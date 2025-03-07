# backend/blog/views.py
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from blog.models import User
from blog.serializer.user import UserSerializer
from django.core.exceptions import ValidationError
from blog.utils.custom_response import custom_response  # 导入自定义响应函数


class RegisterView(APIView):
    """
    用户注册 API
    接收: username, password, email
    返回: 注册成功后的用户信息
    """

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        # 验证输入
        if not username or not password:
            return custom_response(status="error", message="用户名和密码必填", data=None, status_code=status.HTTP_400_BAD_REQUEST)

        if not email:
            return custom_response(status="error", message="邮箱必填", data=None, status_code=status.HTTP_400_BAD_REQUEST)

        # 检查用户名是否重复
        if User.objects.filter(username=username).exists():
            return custom_response(status="error", message="用户名已存在", data=None, status_code=status.HTTP_400_BAD_REQUEST)

        # 检查邮箱是否重复
        if User.objects.filter(email=email).exists():
            return custom_response(status="error", message="邮箱已存在", data=None, status_code=status.HTTP_400_BAD_REQUEST)

        try:
            # 创建用户
            user = User(username=username, email=email)
            user.set_password(password)
            user.save()
            # 序列化返回信息
            serializer = UserSerializer(user)
            return custom_response(data=serializer.data, status_code=status.HTTP_201_CREATED)
        except ValidationError as e:
            return custom_response(status="error", message=str(e), data=None, status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return custom_response(status="error", message="注册失败，请重试", data=None, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    def post(self, request):
        """
        用户登录 API
        接收: username, password
        返回: JWT Token 和用户信息
        """
        username = request.data.get('username')
        password = request.data.get('password')

        # 验证输入
        if not username or not password:
            return custom_response(status="error", message="用户名和密码必填", data=None, status_code=status.HTTP_400_BAD_REQUEST)

        try:
            # 查找用户
            user = User.objects.get(username=username)
            # 验证密码
            if not user.check_password(password):
                return custom_response(status="error", message="用户名或密码错误", data=None, status_code=status.HTTP_401_UNAUTHORIZED)

            if not user.is_active:
                return custom_response(status="error", message="用户已被禁用", data=None, status_code=status.HTTP_403_FORBIDDEN)

            # 生成 JWT Token
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            # 序列化用户信息
            serializer = UserSerializer(user)

            return custom_response(data={
                "token": access_token,
                "refresh_token": refresh_token,
                "user": serializer.data
            }, status_code=status.HTTP_200_OK)

        except User.DoesNotExist:
            return custom_response(status="error", message="用户名或密码错误", data=None, status_code=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return custom_response(status="error", message="登录失败，请重试", data=None, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]  # 需登录权限才能访问

    def get(self, request):
        """
        获取当前用户信息
        接收: 无（需 JWT Token 认证）
        返回: 当前登录用户的信息
        """
        try:
            user = request.user  # 从认证中获取当前用户
            print('user', user)
            serializer = UserSerializer(user)
            return custom_response(data=serializer.data, status_code=status.HTTP_200_OK)
        except Exception as e:
            return custom_response(status="error", message="获取用户信息失败", data=None, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request):
        """修改当前用户信息"""
        try:
            user = request.user
            serializer = UserSerializer(user, data=request.data, partial=True)  # 部分更新
            if serializer.is_valid():
                serializer.save()
                return custom_response(data=serializer.data, status_code=status.HTTP_200_OK)
            return custom_response(status="error", message="参数错误", data=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return custom_response(status="error", message="修改失败，请重试", data=None, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)