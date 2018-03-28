__author__ = 'Daniil Nikulin'
__license__ = "Apache License 2.0"
__email__ = "danil.nikulin@gmail.com"
__date__ = "22.03.2018"
__app__ = "django_rest_social"
__status__ = "Development"

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from posts.models import Post, Like

User = get_user_model()


class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'content',
            'created_at',
            'read_time',
            'posted_by',
            'posted_by_full_name',
            'likes_number',
            'liked_by_users',
        ]

# No need in this class because we use custom Like serializer sp below

# class LikeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Like
#         fields = [
#             'id',
#             'liked_by',
#             'user_id',
#             'liked_by_full_name'
#         ]


def create_like_serializer(post_id, user=None):
    """Custom dynamic serializer for creating Like
    :param post_id:
    :param user:
    :return: CommentCreateSerializer
    """
    class CommentCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = Like
            fields = [
                'id',
                'created_at',
                'post_id',
                'liked_by',
                'liked_by_full_name',
            ]

        def validate(self, data):
            post_qs = Post.objects.filter(id=post_id)
            if not post_qs.exists() and post_qs.count() != 1:
                raise ValidationError("This post does not exist.")
            like_qs = Like.objects.filter(post=post_id, user=user)
            if like_qs.exists() and like_qs.count() >= 1:
                raise ValidationError("This post has been already liked by this user.")
            return data

        def create(self, validated_data):
            like = Like.objects.create(post_id=post_id,
                                       user_id=user.id)
            return like
    return CommentCreateSerializer
