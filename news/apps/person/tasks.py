# -*- coding: utf8 -*-
from news.celeryapp import app as celery_app


@celery_app.task
def add(x, y):
    return x + y
