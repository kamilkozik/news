# -*- coding: utf8 -*-

from django.contrib import admin

from news.apps.common.models import Photo, Gallery


class PhotoAdmin(admin.ModelAdmin):
    pass

admin.site.register(Photo, PhotoAdmin)


class GalleryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Gallery, GalleryAdmin)