# backend/blog/views.py
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from blog.models import Post, Like, Bookmark
from blog.serializer.like import LikeSerializer, CollectionSerializer
from blog.utils.custom_response import custom_response  # 导入自定义响应函数


class LikeView(APIView):
    permission_classes = [IsAuthenticated]  # 需要登录

    def post(self, request):
        """为指定文章点赞"""
        try:
            post_id = request.data.get('post_id')
            if not post_id:
                return custom_response(status="error", message="post_id 不能为空", data=None,
                                       status_code=status.HTTP_400_BAD_REQUEST)
            # 校验文章是否存在且已发布
            post = Post.objects.get(id=post_id, is_published=True)
            user = request.user
            # 检查用户是否已点赞
            like, created = Like.objects.get_or_create(user=user, post=post)
            if not created:
                return custom_response(status="error", message="已点赞，无需重复操作", data=None,
                                       status_code=status.HTTP_400_BAD_REQUEST)
            serializer = LikeSerializer(like)
            return custom_response(data=serializer.data, status_code=status.HTTP_201_CREATED)
        except Post.DoesNotExist:
            return custom_response(status="error", message="文章不存在或未发布", data=None,
                                   status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return custom_response(status="error", message="点赞失败，请重试", data=None,
                                   status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id):
        """取消指定文章的点赞"""
        try:
            # 确认文章存在
            try:
                post = Post.objects.get(id=id)
            except Post.DoesNotExist:
                raise NotFound(detail="文章不存在")

            # 查询点赞记录
            try:
                like = Like.objects.get(post=post, user=request.user)
            except Like.DoesNotExist:
                return custom_response(
                    status="error",
                    message="点赞记录不存在",
                    data=None,
                    status_code=status.HTTP_404_NOT_FOUND
                )

            # 检查权限（确保是用户自己的点赞）
            if like.user != request.user:
                return custom_response(
                    status="error",
                    message="无权限取消此点赞",
                    data=None,
                    status_code=status.HTTP_403_FORBIDDEN
                )

            # 删除点赞记录
            like.delete()

            return custom_response(
                message="取消点赞成功",
                data={},
                status_code=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            print(f"取消点赞错误: {e}")
            return custom_response(
                status="error",
                message="取消点赞失败，请重试",
                data=None,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CollectionView(APIView):
    permission_classes = [IsAuthenticated]  # 需要登录

    def post(self, request):
        """为指定文章收藏"""
        try:
            post_id = request.data.get('post_id')
            if not post_id:
                return custom_response(status="error", message="post_id 不能为空", data=None,
                                       status_code=status.HTTP_400_BAD_REQUEST)
            # 校验文章是否存在且已发布
            post = Post.objects.get(id=post_id, is_published=True)
            user = request.user
            # 检查用户是否已收藏
            collection, created = Bookmark.objects.get_or_create(user=user, post=post)
            if not created:
                return custom_response(status="error", message="已收藏，无需重复操作", data=None,
                                       status_code=status.HTTP_400_BAD_REQUEST)
            serializer = CollectionSerializer(collection)
            return custom_response(data=serializer.data, status_code=status.HTTP_201_CREATED)
        except Post.DoesNotExist:
            return custom_response(status="error", message="文章不存在或未发布", data=None,
                                   status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return custom_response(status="error", message="收藏失败，请重试", data=None,
                                   status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id):
        """取消指定文章的收藏"""
        try:
            # 确认文章存在
            try:
                post = Post.objects.get(id=id)
            except Post.DoesNotExist:
                raise NotFound(detail="文章不存在")

            # 查询收藏记录
            try:
                bookmark = Bookmark.objects.get(post=post, user=request.user)
            except Bookmark.DoesNotExist:
                return custom_response(
                    status="error",
                    message="收藏记录不存在",
                    data=None,
                    status_code=status.HTTP_404_NOT_FOUND
                )

            # 检查权限（确保是用户自己的收藏）
            if bookmark.user != request.user:
                return custom_response(
                    status="error",
                    message="无权限取消此收藏",
                    data=None,
                    status_code=status.HTTP_403_FORBIDDEN
                )

            # 删除收藏记录
            bookmark.delete()

            return custom_response(
                message="取消收藏成功",
                data={},
                status_code=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            print(f"取消收藏错误: {e}")
            return custom_response(
                status="error",
                message="取消收藏失败，请重试",
                data=None,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PostLikeStatusView(APIView):
    def get_permissions(self):
        return [IsAuthenticated()]  # 仅认证用户可访问

    def get(self, request, pk):
        """获取当前用户对指定文章的点赞和收藏状态"""
        try:
            # 获取文章
            post = Post.objects.get(id=pk)

            # 检查点赞状态
            is_liked = Like.objects.filter(post=post, user=request.user).exists()

            # 返回状态
            return custom_response(
                data={
                    "post_id": post.id,
                    "is_liked": is_liked,
                },
                status_code=status.HTTP_200_OK
            )
        except Post.DoesNotExist:
            raise NotFound(detail="文章不存在")
        except Exception as e:
            print(f"获取点赞状态错误: {e}")
            return custom_response(
                status="error",
                data=None,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PostCollectStatusView(APIView):
    def get_permissions(self):
        return [IsAuthenticated()]  # 仅认证用户可访问

    def get(self, request, pk):
        """获取当前用户对指定文章的点赞和收藏状态"""
        try:
            # 获取文章
            post = Post.objects.get(id=pk)

            # 检查收藏状态
            is_bookmarked = Bookmark.objects.filter(post=post, user=request.user).exists()

            # 返回状态
            return custom_response(
                data={
                    "post_id": post.id,
                    "is_bookmarked": is_bookmarked,
                },
                status_code=status.HTTP_200_OK
            )
        except Post.DoesNotExist:
            raise NotFound(detail="文章不存在")
        except Exception as e:
            print(f"获取收藏状态错误: {e}")
            return custom_response(
                status="error",
                data=None,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
