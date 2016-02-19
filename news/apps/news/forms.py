from django.db import models
from django.forms import ModelForm

from news.apps.news.models import Post, Comment


class PostForm(ModelForm):
    title = models.CharField(null=False, blank=False, max_length=500)
    content = models.TextField(null=False, blank=False)

    class Meta:
        model = Post
        fields = ['title', 'content']


class CommentForm(ModelForm):
    content = models.TextField(max_length=5000, null=False, blank=False)

    class Meta:
        model = Comment
        fields = ['content']