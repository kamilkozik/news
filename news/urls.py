# -*- coding: utf8 -*-

from django.conf.urls import url, include

from news.views import PostList, PostCreate, CommentCreate

urlpatterns = [
    url(r'^$', PostList.as_view(), name='list'),
    url(r'^post/', include([
        url(r'^add/$', PostCreate.as_view(), name='add'),
    ], namespace='post')),

    url(r'^comment/', include([
        url(r'^add/(?P<post_pk>\d+)/$', CommentCreate.as_view(), name='add'),
    ], namespace='comment'))
]
