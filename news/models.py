# -*- coding: utf8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

from person.models import Person


class Post(models.Model):
    title = models.CharField(null=False, blank=False, max_length=500)
    content = models.TextField(null=False, blank=False)
    date_added = models.DateField(auto_now=True)
    date_modified = models.DateField(blank=True, null=True)
    is_authorized = models.BooleanField(default=False)
    is_commentable = models.BooleanField(default=True)
    slug = models.SlugField()
    author = models.ForeignKey(Person)


class Comment(models.Model):
    content = models.TextField(max_length=5000, null=False, blank=False)
    date_added = models.DateField(auto_now=True)
    date_modified = models.DateField(blank=True, null=True)
    is_authorized = models.BooleanField(default=False)
    post = models.ForeignKey(Post, related_name='comments')
    author = models.ForeignKey(Person)
