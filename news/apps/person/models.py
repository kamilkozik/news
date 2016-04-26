# -*- coding: utf8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models

from news.apps.person import consts


class Person(models.Model):
    skin_color = models.CharField(max_length=20, choices=consts.SKIN_COLORS, default='green')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='Person')

    class Meta:
        app_label = 'news'


class PersonImage(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    image = models.ImageField()
    person = models.ForeignKey(Person, related_name='person_image')

    class Meta:
        app_label = 'news'

    def set_name(self, name):
        if not name:
            raise
        self.name = name

    def crop_thumbnail(self):
        image_resolution = consts.IMAGE_SIZES['THUMBNAIL']
        self.image.thumbnail(image_resolution)
