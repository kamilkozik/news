# -*- coding: utf8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone

import consts
from news.apps.common.models import Gallery


class Post(models.Model):
    DRAFT = 1
    OPEN = 2
    ARCHIVED = 3

    STATUS_CHOICES = (
        (DRAFT, u'Robocza',),
        (OPEN, u'Otwarta',),
        (ARCHIVED, u'Archiwalna',),
    )

    title = models.CharField(null=False, blank=False, max_length=500)
    content = models.TextField(null=False, blank=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    category = models.IntegerField(choices=consts.CATEGORIES_CHOICES, default=consts.OTHER)
    status = models.IntegerField(choices=STATUS_CHOICES, default=DRAFT)

    date_added = models.DateField(auto_now=True)
    date_modified = models.DateField(blank=True, null=True)
    is_publicated = models.BooleanField(default=False)
    is_commentable = models.BooleanField(default=True)
    slug = models.SlugField()

    gallery = models.OneToOneField(Gallery, on_delete=models.CASCADE,
                                   null=True, blank=True)

    class Meta:
        app_label = 'news'
        verbose_name = u"Post"
        verbose_name_plural = u"Posty"

    def __str__(self):
        return 'Post id: %s' % (self.id,)

    def _switch_publicated(self):
        self.is_publicated = not self.is_publicated

    def _switch_commentable(self):
        self.is_commentable = not self.is_commentable

    def _set_modification_date(self):
        self.date_modified = timezone.now()

    def get_absolute_url(self):
        return reverse('news:list')

    def publish_post(self):
        if not self.is_publicated:
            self._switch_publicated()

    def make_commentable(self):
        if not self.is_commentable:
            self._switch_commentable()


class Comment(models.Model):
    content = models.TextField(max_length=5000, null=False, blank=False)
    date_added = models.DateField(auto_now=True)
    date_modified = models.DateField(blank=True, null=True)
    is_publicated = models.BooleanField(default=False)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        app_label = 'news'
        verbose_name = u"Komentarz"
        verbose_name_plural = u"Komentarze"

    def __str__(self):
        return ' '.join([u'ID komentarza:', str(self.pk)])

    def get_absolute_url(self):
        return reverse('news:list')

    def _switch_publicated(self):
        self.is_publicated = not self.is_publicated

    def publish_comment(self):
        if not self.is_publicated:
            self._switch_publicated()
