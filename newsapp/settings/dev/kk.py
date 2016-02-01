# -*- coding: utf8 -*-

from newsapp.settings.base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'news',
        'USER': 'kamil',
        'HOST': 'localhost',
        'PORT': '',
        'PASSWORD': 'zaq12wsx',
    }
}
