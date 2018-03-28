__author__ = 'Daniil Nikulin'
__license__ = "Apache License 2.0"
__email__ = "danil.nikulin@gmail.com"
__date__ = "28.03.2018"
__app__ = "django_rest_social"
__status__ = "Development"

from django.urls import re_path
from accounts.views import index_view, login_view

urlpatterns = [
    re_path(r'^$', index_view, name='index'),
    re_path(r'^login/$', login_view),
]
