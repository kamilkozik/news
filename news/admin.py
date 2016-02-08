# -*- coding: utf8 -*-

from django.contrib import admin
from django.core.urlresolvers import reverse

from news.models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    fields = ('title', 'content', 'is_authorized', 'author')
    raw_id_fields = ('author',)
    list_display = ('__str__', 'title', 'date_added', 'date_modified',
                    'is_authorized', 'is_commentable', 'author')
    list_filter = ('is_authorized', 'date_added', 'author__username')
    search_fields = ['author__username']


class CommentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'date_added', 'date_modified', 'is_authorized', 'author')
    list_filter = ('is_authorized', 'date_added', 'author__username')

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
