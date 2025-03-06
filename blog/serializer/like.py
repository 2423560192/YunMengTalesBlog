from rest_framework import serializers

from blog.models import Like, Bookmark


class LikeSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    post_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'user_id', 'post_id']
        read_only_fields = ['user_id', 'post_id']
class CollectionSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    post_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Bookmark
        fields = ['id', 'user_id', 'post_id']
        read_only_fields = ['user_id', 'post_id']