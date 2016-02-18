# -*- coding: utf8 -*-

from django.contrib import admin

from news.apps.person.models import Person


class PersonAdmin(admin.ModelAdmin):
    pass

admin.site.register(Person, PersonAdmin)