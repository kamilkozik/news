# -*- coding: utf8 -*-

from django.contrib import admin
from news.apps.common.models import Photo, Gallery


class PhotoAdmin(admin.ModelAdmin):
    fields = ('image', 'title', 'author', 'slug',
              'date_added', 'is_public', 'homepage')
    list_display = ('title', 'author', 'is_public', 'homepage')
    prepopulated_fields = {'slug': ('title',)}

    def save_model(self, request, obj, form, change):
        obj = Photo.set_as_homepage(obj)
        super(PhotoAdmin, self).save_model(request, obj, form, change)

admin.site.register(Photo, PhotoAdmin)


class GalleryAdmin(admin.ModelAdmin):
    fields = ('title', 'author', 'date_added', 'slug',
              'is_public', 'description', 'photos')
    prepopulated_fields = {'slug': ('title',)}

    def get_form(self, request, obj=None, **kwargs):
        form = super(GalleryAdmin, self).get_form(request, obj=None, **kwargs)
        form.base_fields['photos'].queryset = form.base_fields['photos']\
            .queryset.filter(author=request.user)
        return form

admin.site.register(Gallery, GalleryAdmin)
