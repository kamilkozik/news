# -*- coding: utf8 -*-

from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.conf import settings

from news.apps.news.views import auth_view, log_in, log_out

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', RedirectView.as_view(pattern_name='news:list')),
    url(r'^news/', include('news.apps.news.urls', namespace='news')),

    # Authentication
    url(r'^auth/login/', include([
        url(r'^$', auth_view, name='auth_view'),
        url(r'^log_in/$', log_in, name='log_in'),
        url(r'^log_out/$', log_out, name='log_out')
    ])),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
