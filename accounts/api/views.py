__author__ = 'Daniil Nikulin'
__license__ = "Apache License 2.0"
__email__ = "danil.nikulin@gmail.com"
__date__ = "22.03.2018"
__app__ = "django_rest_social"
__status__ = "Development"

from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from . import serializers

User = get_user_model()


class UserCreateAPIView(CreateAPIView):
    serializer_class = serializers.UserCreateSerializer
    permission_classes = [AllowAny]
