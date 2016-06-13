# -*- coding: utf8 -*-

from __future__ import unicode_literals

import os

from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import force_text
from django.utils.text import slugify
from django.utils.timezone import now
from sortedm2m.fields import SortedManyToManyField

from news.apps.common.helpers import get_files_upload_path

import consts


class ImageModel(models.Model):
    image = models.ImageField(u'obraz',
                              max_length=consts.IMAGE_FIELD_MAX_LENGTH,
                              upload_to=get_files_upload_path)
    view_count = models.PositiveIntegerField(u'liczba wyświetleń',
                                             default=0,
                                             editable=False)

    class Meta:
        app_label = 'news'
        abstract = True

    def image_filename(self):
        return os.path.basename(force_text(self.image.name))

    def increment_count(self):
        self.view_count += 1
        models.Model.save(self)


class Photo(ImageModel):
    title = models.CharField(u'tytuł', max_length=250, null=False, blank=False)
    author = models.ForeignKey(User, null=False, blank=False)
    date_added = models.DateTimeField(u'dodano', default=now)
    slug = models.SlugField(u'slug', unique=True, max_length=250)
    is_public = models.BooleanField(u'czy publiczny?', default=True)

    class Meta:
        app_label = 'news'
        ordering = ['-date_added']
        get_latest_by = 'date_added'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not len(self.slug):
            self.slug = slugify(self.title)

        # Check if created slug already exists. Handle duplicates
        super(Photo, self).save(*args, **kwargs)


class Gallery(models.Model):
    title = models.CharField(u'tytuł', max_length=250, unique=True)
    author = models.ForeignKey(User, null=False, blank=False)
    date_added = models.DateTimeField(u'dodano', default=now)
    slug = models.SlugField(u'slug', unique=True, max_length=250)
    is_public = models.BooleanField(u'czy publiczna?', default=True)

    description = models.TextField(u'opis', blank=True, null=True)
    photos = SortedManyToManyField(Photo,
                                   related_name=u'galleries',
                                   verbose_name=u'zdjęcia',
                                   blank=True)

    class Meta:
        app_label = 'news'
        ordering = ['-date_added']
        get_latest_by = 'date_added'

    def __str__(self):
        return self.title
