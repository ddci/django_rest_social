from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save

from posts.utils import get_read_time


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    read_time = models.IntegerField(default=0)

    class Meta:
        ordering = ["-created_at"]

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    @property
    def posted_by(self):
        user = self.user
        return "{}".format(user.username)

    @property
    def posted_by_full_name(self):
        user = self.user
        return "{} {}".format(user.first_name, user.last_name)

    @property
    def likes_number(self):
        likes_num = Like.objects.filter(post=self.id).count()
        return likes_num

    @property
    def liked_by_users(self):
        users_list = []
        # likes_qs = Like.objects.filter(post=self.id).order_by("-created_at")[:10]
        likes_qs = Like.objects.filter(post=self.id).order_by("-created_at")
        users_list = [like.liked_by for like in likes_qs]
        return users_list


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    @property
    def liked_by(self):
        user = self.user
        return "{}".format(user.username)

    @property
    def liked_by_full_name(self):
        user = self.user
        return "{} {}".format(user.first_name, user.last_name)


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if instance.content:
        html_string = instance.content
        read_time_var = get_read_time(html_string)
        instance.read_time = read_time_var


pre_save.connect(pre_save_post_receiver, sender=Post)
