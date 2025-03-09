from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from blog.models import Category
from blog.serializer.post import CategorySerializer
from blog.utils.custom_response import custom_response  # 导入自定义响应函数


class CategoryListView(APIView):
    def get_permissions(self):
        return [AllowAny()]  # 公开访问

    def get(self, request):
        """获取所有分类列表（公开访问）"""
        try:
            # 获取所有分类，按创建时间倒序
            categories = Category.objects.all().order_by('-created_at')
            # 序列化数据
            serializer = CategorySerializer(categories, many=True)
            return custom_response(
                data=serializer.data,
                status_code=status.HTTP_200_OK
            )
        except Exception as e:
            print(e)
            return custom_response(
                status="error",
                message="获取分类列表失败",
                data=None,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
