# -*- coding: utf8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from consts import SKIN_COLORS


class Person(models.Model):
    skin_color = models.CharField(max_length=20, choices=SKIN_COLORS, default='green')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='Person')

    class Meta:
        app_label = 'news'
