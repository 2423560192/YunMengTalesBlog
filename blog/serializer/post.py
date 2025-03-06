# backend/blog/serializers.py
from rest_framework import serializers
from blog.models import Post, Category, Tag
from blog.serializer.user import UserSerializer  # 假设有 User 的序列化器


class TagSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)  # 只读，来自数据库
    name = serializers.CharField(max_length=12, min_length=2, error_messages={
        'max_length': '标签名称不能超过 12 个字符',
        'min_length': '标签名称至少需要 2 个字符',
        'required': '标签名称是必填字段',
        'blank': '标签名称不能为空'
    })  # 长度限制 2-6 字符

    def create(self, validated_data):
        # 创建新 Tag 实例，跳过 unique=True 验证
        name = validated_data['name']
        tag, _ = Tag.objects.get_or_create(name=name)
        return tag

    def update(self, instance, validated_data):
        # 更新 Tag 实例，跳过 unique=True 验证
        instance.name = validated_data.get('name', instance.name, )
        instance.save()
        return instance


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)  # 只读，来自数据库
    name = serializers.CharField(max_length=12, min_length=2, error_messages={
        'max_length': '标签名称不能超过 12 个字符',
        'min_length': '标签名称至少需要 2 个字符',
        'required': '标签名称是必填字段',
        'blank': '标签名称不能为空'
    })  # 长度限制 2-6 字符

    def create(self, validated_data):
        # 创建新 Category 实例，跳过 unique=True 验证
        name = validated_data['name']
        category, _ = Category.objects.get_or_create(name=name)
        return category

    def update(self, instance, validated_data):
        # 更新 Category 实例，跳过 unique=True 验证
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class PostSerializer(serializers.ModelSerializer):
    # author 字段使用 UserSerializer 序列化，只读模式，用于显示作者信息
    author = UserSerializer(read_only=True)
    # category 字段使用 CategorySerializer 序列化，用于展示和处理分类信息
    category = CategorySerializer()
    # tags 字段使用 TagSerializer 序列化，many=True 表示多对多关系，支持多个标签
    tags = TagSerializer(many=True)

    class Meta:
        model = Post  # 指定关联的模型为 Post
        fields = [  # 指定序列化时包含的字段列表
            'id',  # 文章ID
            'title',  # 文章标题
            'content',  # 文章内容
            'cover',  # 文章封面图片
            'author',  # 作者信息
            'category',  # 分类信息
            'tags',  # 标签列表
            'created_at',  # 创建时间
            'updated_at',  # 更新时间
            'is_published'  # 是否发布状态
        ]

    def create(self, validated_data):
        """
        创建文章的方法
        参数: validated_data (dict): 经过验证的输入数据，包含文章相关信息
        返回: Post: 创建完成的文章实例
        """
        # 从 validated_data 中提取并移除 category 数据
        category_data = validated_data.pop('category')

        # 从 validated_data 中提取并移除 tags 数据，默认为空列表
        tags_data = validated_data.pop('tags', [])

        # 获取或创建分类对象，如果已存在则获取，不存在则创建
        category, _ = Category.objects.get_or_create(name=category_data['name'])

        # 创建文章实例
        post = Post.objects.create(
            title=validated_data['title'],  # 设置文章标题
            content=validated_data['content'],  # 设置文章内容
            cover=validated_data.get('cover', ''),  # 设置封面图片，默认值为空字符串
            author=self.context['request'].user,  # 设置作者为当前登录用户
            category=category,  # 设置文章分类
            is_published=validated_data.get('is_published', True)  # 设置发布状态，默认True
        )

        # 遍历标签数据，为文章添加标签
        for tag_data in tags_data:
            # 获取或创建标签对象，如果已存在则获取，不存在则创建
            tag, _ = Tag.objects.get_or_create(name=tag_data['name'])
            # 将标签添加到文章的多对多关系中
            post.tags.add(tag)

        # 返回创建完成的文章实例
        return post

    def update(self, instance, validated_data):
        """更简洁的更新文章：直接覆盖所有字段，category 和 tags 用 get_or_create"""
        # 直接覆盖所有字段（如果传了就用新值，没传保留原值）
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.cover = validated_data.get('cover', instance.cover)
        instance.is_published = validated_data.get('is_published', instance.is_published)

        # 简化为直接用 get_or_create 处理 category（无论是否变化）
        category_data = validated_data.pop('category', None)
        if category_data:
            category, _ = Category.objects.get_or_create(name=category_data['name'])
            instance.category = category

        # 简化为直接用 get_or_create 处理 tags（无论是否变化）
        tags_data = validated_data.pop('tags', None)
        if tags_data is not None:
            instance.tags.clear()  # 清空旧标签
            for tag_data in tags_data:
                tag, _ = Tag.objects.get_or_create(name=tag_data['name'])
                instance.tags.add(tag)

        instance.save()
        return instance


