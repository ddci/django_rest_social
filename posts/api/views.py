__author__ = 'Daniil Nikulin'
__license__ = "Apache License 2.0"
__email__ = "danil.nikulin@gmail.com"
__date__ = "22.03.2018"
__app__ = "django_rest_social"
__status__ = "Development"

from rest_framework import permissions
from rest_framework import viewsets, status, mixins
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from posts.api import serializers
from posts.api.pagination import PostPageNumberPagination, LikePageNumberPagination
from posts.api.serializers import create_like_serializer
from posts.models import Post, Like


class PostCreateListRetrieveViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                                    mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = serializers.PostDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PostPageNumberPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # def list(self, request, **kwargs):
    #     queryset = Post.objects.all()
    #     serializer = serializers.PostDetailSerializer(queryset, many=True)
    #     return Response(serializer.data)

    def retrieve(self, request, pk=None, **kwargs):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, pk=pk)
        serializer = serializers.PostDetailSerializer(post)
        return Response(serializer.data)


class LikeCreateListDeleteViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                                  mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Like.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    # lookup_field = 'post_id'
    lookup_url_kwarg = 'post_id'
    pagination_class = LikePageNumberPagination

    def perform_create(self, serializer):
        post_id = self.kwargs.get(self.lookup_url_kwarg)
        serializer.save(user_id=self.request.user.id, post_id=post_id)

    def list(self, request, **kwargs):
        post_id = self.kwargs.get(self.lookup_url_kwarg)
        queryset = Like.objects.filter(post_id=post_id).order_by("-created_at")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        post_id = self.kwargs.get(self.lookup_url_kwarg)
        return create_like_serializer(
            post_id=post_id,
            user=self.request.user
        )

    def destroy(self, request, *args, **kwargs):
        post_id = self.kwargs.get(self.lookup_url_kwarg)
        like_instance = Like.objects.get(post_id=post_id, user_id=self.request.user.id)
        self.perform_destroy(like_instance)
        return Response("Successfully deleted like.", status=status.HTTP_204_NO_CONTENT)
