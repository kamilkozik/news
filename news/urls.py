# -*- coding: utf8 -*-

from django.conf.urls import url

from news.views import PostList, PostCreate

urlpatterns = [
    url(r'^$', PostList.as_view(), name='list'),
    url(r'^add/$', PostCreate.as_view(), name='add'),
]
