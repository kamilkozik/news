# -*- coding: utf8 -*-

from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from news.apps.news.views import *

urlpatterns = [
    # Admin
    url(r'^admin/', admin.site.urls),

    # Homepage
    url(r'^$', homepage, name='homepage'),

    # Person
    url(r'^person/', include('news.apps.person.urls', namespace='person')),

    # News
    url(r'^news/', include('news.apps.news.urls', namespace='news')),

    # Authentication
    url(r'^auth/', include([

        url(r'^log/', include([
            url(r'^$', auth_view, name='show'),
            url(r'^in/$', log_in, name='log_in'),
            url(r'^out/$', log_out, name='log_out')
        ], namespace='auth')),

        url(r'^register/', include([
            url(r'^$', register_view, name='show'),
            url(r'^add/$', register, name='add')
        ], namespace='register')),

        # Social auth
        url('', include('social.apps.django_app.urls', namespace='social'))
    ])),

    url(r'^flush_session/$', flush_session_values, name='flush_session'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
