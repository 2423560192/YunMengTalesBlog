import json

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from blog.models import Post, Tag, Category
from blog.serializer.post import PostSerializer
from blog.utils.custom_response import custom_response  # 导入自定义响应函数
from blog.utils.pages import PostPagination  # 导入分页类


class PostListCreateView(APIView):
    # 为不同方法设置不同权限
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]  # GET 公开访问
        return [IsAuthenticated()]  # POST 需要登录

    def get(self, request):
        """获取文章列表（支持分页）"""
        # 使用全局分页配置
        paginator = PostPagination()
        posts = Post.objects.filter(is_published=True).all().order_by('-created_at')  # 按创建时间降序
        # 应用分页
        page = paginator.paginate_queryset(posts, request)
        serializer = PostSerializer(page, many=True)

        # 构造分页响应数据
        paginated_data = {
            "count": paginator.page.paginator.count,  # 总记录数
            "next": paginator.get_next_link(),  # 下一页链接
            "previous": paginator.get_previous_link(),  # 上一页链接
            "results": serializer.data  # 当前页的数据
        }
        print('请求：', json.dumps(serializer.data))
        return custom_response(data=serializer.data, status_code=status.HTTP_200_OK)

    def post(self, request):
        """创建新文章"""
        try:
            serializer = PostSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return custom_response(data=serializer.data, status_code=status.HTTP_201_CREATED)
            return custom_response(status="error", message="参数错误", data=serializer.errors,
                                   status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return custom_response(status="error", message="创建文章失败，请重试", data=None,
                                   status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PostDetailView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]  # GET 公开访问
        return [IsAuthenticated()]  # PUT/DELETE 需要登录

    def get(self, request, pk):
        """获取文章详情（公开访问）"""
        try:
            post = Post.objects.get(id=pk, is_published=True)  # 只返回已发布的文章
            serializer = PostSerializer(post)
            return custom_response(data=serializer.data, status_code=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return custom_response(status="error", message="文章不存在", data=None,
                                   status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return custom_response(status="error", message="获取文章详情失败", data=None,
                                   status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
            if post.author != request.user:
                return custom_response(status="error", message="无权限更新此文章", data=None,
                                       status_code=status.HTTP_403_FORBIDDEN)

            serializer = PostSerializer(post, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return custom_response(data=serializer.data, status_code=status.HTTP_200_OK)
            return custom_response(status="error", message="参数错误", data=serializer.errors,
                                   status_code=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            return custom_response(status="error", message="文章不存在", data=None,
                                   status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return custom_response(status="error", message="更新文章失败，请重试", data=None,
                                   status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        """删除文章（需登录，限制作者）"""
        try:
            post = Post.objects.get(id=pk)
            if post.author != request.user:
                return custom_response(status="error", message="无权限删除此文章", data=None,
                                       status_code=status.HTTP_403_FORBIDDEN)
            post.delete()
            return custom_response(message="删除成功", data={}, status_code=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist:
            return custom_response(status="error", message="文章不存在", data=None,
                                   status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return custom_response(status="error", message="删除文章失败，请重试", data=None,
                                   status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PostFilterView(APIView):
    def get_permissions(self):
        return [AllowAny()]

    def get(self, request):
        try:
            category_name = request.GET.get('category_name')
            tag_name = request.GET.get('tag_name')

            if not category_name and not tag_name:
                return custom_response(
                    status="error",
                    message="至少需要提供 category_name 或 tag_name",
                    data=None,
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            posts = Post.objects.filter(is_published=True).order_by('-created_at')

            if category_name:
                category = Category.objects.get(name=category_name)
                posts = posts.filter(category=category)

            if tag_name:
                tag = Tag.objects.get(name=tag_name)
                posts = posts.filter(tags=tag)

            paginator = PostPagination()
            page = paginator.paginate_queryset(posts, request)
            serializer = PostSerializer(page, many=True)
            return custom_response(
                data=serializer.data,
                status_code=status.HTTP_200_OK
            )
        except Category.DoesNotExist:
            return custom_response(
                status="error",
                message="分类不存在",
                data=None,
                status_code=status.HTTP_404_NOT_FOUND
            )
        except Tag.DoesNotExist:
            return custom_response(
                status="error",
                message="标签不存在",
                data=None,
                status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            print(e)
            return custom_response(
                status="error",
                message="获取文章列表失败",
                data=None,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
