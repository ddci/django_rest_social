__author__ = 'Daniil Nikulin'
__license__ = "Apache License 2.0"
__email__ = "danil.nikulin@gmail.com"
__date__ = "22.03.2018"
__app__ = "django_rest_social"
__status__ = "Development"

from django.urls import re_path

from posts.api.views import PostCreateListRetrieveViewSet, LikeCreateListDeleteViewSet

urlpatterns = [
    re_path(r'^(?P<post_id>\d+)/likes/$', LikeCreateListDeleteViewSet.as_view({'get': 'list',
                                                                               'post': 'create',
                                                                               'delete': 'destroy'}), name='likes'),
    # re_path(r'^(?P<post_pk>\d+)/likes/(?P<like_pk>\d+)', LikeCreateDelete.as_view({'get': 'retrieve',
    #                                                                                'post': 'create'}), name='like'),
    re_path(r'^(?P<pk>\d+)/$', PostCreateListRetrieveViewSet.as_view({'get': 'retrieve'}), name='posts'),
    re_path(r'^$', PostCreateListRetrieveViewSet.as_view({'get': 'list',
                                                          'post': 'create'}), name='posts'),
]
