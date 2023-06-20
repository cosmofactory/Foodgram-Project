from rest_framework.pagination import PageNumberPagination


class PageSizePagination(PageNumberPagination):
    """Custom pagination defining limit."""

    page_size = 10
    page_size_query_param = 'limit'
    max_page_size = 100
