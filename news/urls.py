# -*- coding: utf8 -*-

from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.conf import settings

from news.apps.news.views import auth_view, log_in, log_out, flush_session_values, register, register_view

urlpatterns = [
    # Admin
    url(r'^admin/', admin.site.urls),

    # News
    url(r'^$', RedirectView.as_view(pattern_name='news:list')),
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
        ], namespace='register'))
    ])),

    url(r'^flush_session/$', flush_session_values, name='flush_session'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
