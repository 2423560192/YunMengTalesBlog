# backend/blog/views.py
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from blog.models import Post, Comment
from blog.serializer.comment import CommentSerializer
from blog.utils.custom_response import custom_response  # 导入自定义响应函数
from blog.utils.pages import CommentPagination


class CommentListView(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]  # GET 公开访问
        return [IsAuthenticated()]  # POST 需要登录

    def get(self, request):
        """获取指定文章的评论列表（公开访问）"""
        try:
            # 获取文章id
            post_id = request.GET.get('post_id')
            if not post_id:
                return custom_response(status="error", message="文章 id 不能为空", data=None, status_code=status.HTTP_400_BAD_REQUEST)
            # 校验文章是否存在
            post = Post.objects.get(id=post_id, is_published=True)
            # 获取评论，按创建时间倒序
            comments = Comment.objects.filter(post=post).order_by('-created_at')

            # 分页
            paginator = CommentPagination()
            page = paginator.paginate_queryset(comments, request)
            serializer = CommentSerializer(page, many=True)

            return custom_response(data=serializer.data, status_code=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return custom_response(status="error", message="文章不存在", data=None, status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return custom_response(status="error", message="获取评论列表失败", data=None, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """为指定文章创建评论"""
        try:
            # 校验文章是否存在且已发布
            post_id = request.data.get('post_id')
            Post.objects.get(id=post_id, is_published=True)

            # 序列化数据，传递 post_id 给 serializer
            serializer = CommentSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return custom_response(data=serializer.data, status_code=status.HTTP_201_CREATED)
            return custom_response(status="error", message="参数错误", data=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            return custom_response(status="error", message="文章不存在或未发布", data=None, status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return custom_response(status="error", message="创建评论失败，请重试", data=None, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CommentDeleteView(APIView):
    permission_classes = [IsAuthenticated]  # 需要登录

    def delete(self, request, pk):
        """删除指定评论（需登录，限制作者）"""
        try:
            # 获取评论
            comment = Comment.objects.get(id=pk)
            # 校验权限：只允许作者删除
            if comment.user != request.user:
                return custom_response(status="error", message="无权限删除此评论", data=None, status_code=status.HTTP_403_FORBIDDEN)
            # 删除评论及其所有子评论
            self._delete_comment_and_children(comment)
            return custom_response(message="删除成功", data={}, status_code=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist:
            return custom_response(status="error", message="评论不存在", data=None, status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return custom_response(status="error", message="删除评论失败，请重试", data=None, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _delete_comment_and_children(self, comment):
        """递归删除评论及其所有子评论"""
        children = Comment.objects.filter(parent=comment)
        for child in children:
            self._delete_comment_and_children(child)
        comment.delete()