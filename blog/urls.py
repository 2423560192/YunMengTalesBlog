from django.urls import path

from blog.views.like import LikeView, CollectionView
from blog.views.post import PostListCreateView, PostDetailView
from blog.views.user import RegisterView, LoginView, UserDetailView
from blog.views.comment import CommentListView, CommentDeleteView

urlpatterns = [
    # 用户相关
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('user/', UserDetailView.as_view(), name='user'),
    # 文章相关
    path('posts/', PostListCreateView.as_view(), name='post'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),  # 详情获取和更新

    # 评论相关
    path('comments/', CommentListView.as_view(), name='comment'),
    path('comments/<int:pk>/', CommentDeleteView.as_view(), name='comment-delete'),  # 删除评论

    # 点赞相关
    path('like/', LikeView.as_view(), name='like-create'),  # 点赞文章
    path('like/<int:id>/', LikeView.as_view(), name='like-delete'),  # 取消点赞

    # 收藏相关
    path('collect/', CollectionView.as_view(), name='collect-create'),  # 收藏文章
    path('collect/<int:id>/', CollectionView.as_view(), name='collect-delete'),  # 取消收藏
]
