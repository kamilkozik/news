# -*- coding: utf8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone


class Post(models.Model):
    title = models.CharField(null=False, blank=False, max_length=500)
    content = models.TextField(null=False, blank=False)
    date_added = models.DateField(auto_now=True)
    date_modified = models.DateField(blank=True, null=True)
    is_authorized = models.BooleanField(default=False)
    is_commentable = models.BooleanField(default=True)
    slug = models.SlugField()
    author = models.ForeignKey(User)

    class Meta:
        verbose_name = u"Post"
        verbose_name_plural = u"Posty"

    def __str__(self):
        return 'Post id: %s' % (self.id,)

    def _switch_authorize(self):
        self.is_authorized = (not self.is_authorized)

    def _set_modification_date(self):
        self.date_modified = timezone.now()

    def _switch_commentable(self):
        self.is_commentable = not self.is_commentable

    def get_absolute_url(self):
        return reverse('news:list')


class Comment(models.Model):
    content = models.TextField(max_length=5000, null=False, blank=False)
    date_added = models.DateField(auto_now=True)
    date_modified = models.DateField(blank=True, null=True)
    is_authorized = models.BooleanField(default=False)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User)

    class Meta:
        verbose_name = u"Komentarz"
        verbose_name_plural = u"Komentarze"

    def __str__(self):
        return ' '.join([u'ID komentarza:', str(self.pk)])

    def get_absolute_url(self):
        return reverse('news:list')
