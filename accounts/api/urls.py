__author__ = 'Daniil Nikulin'
__license__ = "Apache License 2.0"
__email__ = "danil.nikulin@gmail.com"
__date__ = "22.03.2018"
__app__ = "django_rest_social"
__status__ = "Development"

from django.urls import re_path, path

from .views import UserCreateAPIView

urlpatterns = [
    # other urls before this
    re_path(r'^$', UserCreateAPIView.as_view(), name='register'),
]
