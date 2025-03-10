from rest_framework import serializers

from blog.models import Comment, Post
from blog.serializer.user import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    post_id = serializers.IntegerField()
    # parent_id = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), allow_null=True, required=False,)
    parent_id = serializers.IntegerField(required=False ,allow_null = True)
    children = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user', 'post_id', 'parent_id', 'created_at', 'children']
        read_only_fields = ['user', 'created_at']

    def get_children(self, obj):
        """获取子评论（嵌套）"""
        children = Comment.objects.filter(parent=obj).order_by('-created_at')
        return CommentSerializer(children, many=True, context=self.context).data

    def create(self, validated_data):
        """创建评论，关联当前用户和文章，支持父评论"""
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("需要登录才能创建评论")
        print('校验后的数据', validated_data)
        post_id = validated_data['post_id']
        try:
            post = Post.objects.get(id=post_id, is_published=True)
            print('文章：', post)
        except Post.DoesNotExist:
            raise serializers.ValidationError("文章不存在或未发布")

        parent_id = validated_data.pop('parent_id', None)
        if parent_id and not Comment.objects.filter(id=parent_id, post=post).exists():
            raise serializers.ValidationError("父评论无效或不属于此文章")

        return Comment.objects.create(
            content=validated_data['content'],
            user=request.user,
            post=post,
            parent_id=parent_id
        )
