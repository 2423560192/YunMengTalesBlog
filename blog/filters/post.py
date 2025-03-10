# backend/blog/filters.py
from django_filters import FilterSet, CharFilter
from blog.models import Post


class PostFilter(FilterSet):
    keyword = CharFilter(field_name='content', lookup_expr='icontains', label='全文过滤关键词')

    class Meta:
        model = Post
        fields = ['keyword']
