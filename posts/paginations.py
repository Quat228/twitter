from rest_framework import pagination


class TweetNumberPagination(pagination.PageNumberPagination):
    page_size = 1
    max_page_size = 100
