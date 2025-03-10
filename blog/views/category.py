from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from blog.models import Category, Post
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
class CategoryPostCountView(APIView):
    def get_permissions(self):
        return [AllowAny()]  # 公开访问

    def get(self, request):
        """根据分类名称计算该分类下文章数量（公开访问）"""
        try:
            # 获取查询参数
            category_name = request.GET.get('category_name')

            # 校验参数
            if not category_name:
                return custom_response(
                    status="错误",
                    message="分类名称不能为空",
                    data=None,
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            # 校验分类是否存在
            category = Category.objects.get(name=category_name)

            # 计算该分类下已发布的文章数量
            post_count = Post.objects.filter(category=category, is_published=True).count()

            # 返回数据
            return custom_response(
                data={
                    "category_name": category_name,
                    "post_count": post_count
                },
                status_code=status.HTTP_200_OK
            )
        except Category.DoesNotExist:
            return custom_response(
                status="错误",
                message="分类不存在",
                data=None,
                status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            print(e)
            return custom_response(
                status="错误",
                message="计算文章数量失败",
                data=None,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )