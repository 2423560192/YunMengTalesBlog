from rest_framework.pagination import PageNumberPagination


class PostPagination(PageNumberPagination):
    """
    全局分页配置类，用于文章、评论等列表的分页。
    """
    page_size = 10  # 每页 10 条
    page_size_query_param = 'page_size'  # 支持自定义每页条数，如 ?page_size=20
    max_page_size = 100  # 最大每页条数

class CommentPagination(PostPagination):
    """
    自定义分页配置类，用于评论列表的分页。
    继承 PostPagination，调整 page_size 以适应评论的显示需求。
    """
    page_size = 20  # 每页 20 条（适合评论列表，假设评论量较大）