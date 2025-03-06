from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.models import Post, Comment
from blog.serializer.comment import CommentSerializer


class CommentListPagination(PageNumberPagination):
    page_size = 10  # 每页 10 条
    page_size_query_param = 'page_size'  # 支持自定义每页条数
    max_page_size = 100  # 最大每页条数


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
                return Response({"error": "文章 id 不能为空"}, status=status.HTTP_400_BAD_REQUEST)
            # 校验文章是否存在
            post = Post.objects.get(id=post_id, is_published=True)
            # 获取评论，按创建时间倒序
            comments = Comment.objects.filter(post=post).order_by('-created_at')
            # 分页
            paginator = CommentListPagination()
            page = paginator.paginate_queryset(comments, request)
            serializer = CommentSerializer(page, many=True)

            return paginator.get_paginated_response(serializer.data)
        except Post.DoesNotExist:
            return Response({"error": "文章不存在"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "获取评论列表失败"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            return Response({"error": "文章不存在或未发布"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"error": "创建评论失败，请重试"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CommentDeleteView(APIView):
    permission_classes = [IsAuthenticated]  # 需要登录

    def delete(self, request, pk):
        """删除指定评论（需登录，限制作者）"""
        try:
            # 获取评论
            comment = Comment.objects.get(id=pk)
            # 校验权限：只允许作者删除
            if comment.user != request.user:
                return Response({"error": "无权限删除此评论"}, status=status.HTTP_403_FORBIDDEN)
            # 删除评论及其所有子评论
            self._delete_comment_and_children(comment)
            return Response({'msg': "删除成功"}, status=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist:
            return Response({"error": "评论不存在"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"error": "删除评论失败，请重试"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _delete_comment_and_children(self, comment):
        """递归删除评论及其所有子评论"""
        children = Comment.objects.filter(parent=comment)
        for child in children:
            self._delete_comment_and_children(child)
        comment.delete()
