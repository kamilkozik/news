# -*- coding: utf8 -*-

from django.conf.urls import url

from news.views import PostList

urlpatterns = [
    url(r'^$', PostList.as_view(), name='list')
]
