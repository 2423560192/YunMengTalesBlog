# backend/blog/views.py
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from blog.models import Tag
from blog.serializer.post import TagSerializer

from blog.utils.custom_response import custom_response  # 导入自定义响应函数
from blog.utils.pages import CommentPagination  # 假设你有分页工具


class TagListView(APIView):
    def get_permissions(self):
        return [AllowAny()]  # 公开访问

    def get(self, request):
        """获取所有标签列表（公开访问）"""
        try:
            # 获取所有标签
            tags = Tag.objects.all().order_by('name')

            # 应用分页（可选）
            paginator = CommentPagination()
            page = paginator.paginate_queryset(tags, request)
            serializer = TagSerializer(page, many=True)

            return custom_response(
                data=serializer.data,
                status_code=status.HTTP_200_OK
            )
        except Exception as e:
            print(e)
            return custom_response(
                status="错误",
                message="获取标签列表失败",
                data=None,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )