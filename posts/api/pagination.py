__author__ = 'Daniil Nikulin'
__license__ = "Apache License 2.0"
__email__ = "danil.nikulin@gmail.com"
__date__ = "24.03.2018"
__app__ = "django_rest_social"
__status__ = "Development"

from rest_framework import pagination


class PostPageNumberPagination(pagination.PageNumberPagination):
    page_size = 10


class LikePageNumberPagination(pagination.PageNumberPagination):
    page_size = 50
