# -*- coding: utf8 -*-

from django.conf.urls import url, include

from news.apps.person.views import settings as profile_settings, add_image

urlpatterns = [
    # Person
    url(r'^profile/', include([
        url(r'^$', profile_settings, name='show'),
        url(r'^image/', include([

            url(r'^add/$', add_image, name='add'),

        ], namespace='image')),
    ], namespace="profile"))
]
