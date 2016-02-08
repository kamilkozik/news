# -*- coding: utf8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models


class Post(models.Model):
    title = models.CharField(null=False, blank=False, max_length=500)
    content = models.TextField(null=False, blank=False)
    date_added = models.DateField(auto_now=True)
    date_modified = models.DateField(blank=True, null=True)
    is_authorized = models.BooleanField(default=False)
    is_commentable = models.BooleanField(default=True)
    slug = models.SlugField()
    author = models.ForeignKey(User)

    def get_absolute_url(self):
        return reverse('news:list')


class Comment(models.Model):
    content = models.TextField(max_length=5000, null=False, blank=False)
    date_added = models.DateField(auto_now=True)
    date_modified = models.DateField(blank=True, null=True)
    is_authorized = models.BooleanField(default=False)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User)

    def get_absolute_url(self):
        return reverse('news:list')
