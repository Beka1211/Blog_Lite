from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='liked_posts',
        blank=True,
    )
    views_count = models.PositiveIntegerField(default=0)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class SubPost(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='liked_subposts',
        blank=True,
    )
    views_count = models.PositiveIntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='subposts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} (sub to{self.post.title})'



