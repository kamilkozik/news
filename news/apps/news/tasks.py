# -*- coding: utf-8 -*-
from news.apps.news.models import Post
from news.celeryapp import app as celery_app


@celery_app.task
def publish_posts():
    posts = Post.objects.filter(is_publicated=False)
    if posts:
        for post in posts:
            post.publish_post()
            post.save()
    else:
        print 'No posts for publication found.'
