# -*- coding: utf8 -*-

from django.conf.urls import url, include

from news.apps.news.views import PostList, PostCreate, CommentCreate, post_publish, comment_publish, PostDelete, \
    CommentDelete, post_update

urlpatterns = [
    url(r'^$', PostList.as_view(), name='list'),
    url(r'^post/', include([
        url(r'^add/$', PostCreate.as_view(), name='add'),
        url(r'^update/(?P<pk>\d+)/$', post_update, name='update'),
        url(r'^delete/(?P<pk>\d+)/$', PostDelete.as_view(), name='delete'),
        url(r'^publish/(?P<post_pk>\d+)/$', post_publish, name='publish'),
    ], namespace='post')),

    url(r'^comment/', include([
        url(r'^add/(?P<post_pk>\d+)/$', CommentCreate.as_view(), name='add'),
        url(r'^delete/(?P<pk>\d+)/$', CommentDelete.as_view(), name='delete'),
        url(r'^publish/(?P<comment_pk>\d+)/$', comment_publish, name='publish')
    ], namespace='comment'))
]
