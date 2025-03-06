# backend/blog/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from blog.models import Post
from blog.serializer.post import PostSerializer


class PostListCreateView(APIView):
    # 为不同方法设置不同权限
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]  # GET 公开访问
        return [IsAuthenticated()]  # POST 需要登录

    def get(self, request):
        """获取文章列表"""
        posts = Post.objects.all().order_by('-created_at')  # 按创建时间降序
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """创建新文章"""
        try:
            serializer = PostSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "创建文章失败，请重试"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PostDetailView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]  # GET 公开访问
        return [IsAuthenticated()]  # POST 需要登录

    def get(self, request, pk):
        """获取文章详情（公开访问）"""
        try:
            post = Post.objects.get(id=pk, is_published=True)  # 只返回已发布的文章
            serializer = PostSerializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({"error": "文章不存在"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "获取文章详情失败"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
            if post.author != request.user:
                return Response({"error": "无权限更新此文章"}, status=status.HTTP_403_FORBIDDEN)

            serializer = PostSerializer(post, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            return Response({"error": "文章不存在"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "更新文章失败，请重试"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        """删除文章（需登录，限制作者）"""
        try:
            post = Post.objects.get(id=pk)
            if post.author != self.request.user:
                return Response({"error": "无权限删除此文章"}, status=status.HTTP_403_FORBIDDEN)
            post.delete()
            return Response({"msg": "删除成功"}, status=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist:
            return Response({"error": "文章不存在"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "删除文章失败，请重试"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
