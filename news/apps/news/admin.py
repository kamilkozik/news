# -*- coding: utf8 -*-

from django.contrib import admin

from news.apps.common.models import Gallery
from news.apps.news.models import Post, Comment


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 1


class PostAdmin(admin.ModelAdmin):
    fields = ('title', 'content', 'is_publicated', 'author', 'gallery')
    raw_id_fields = ('author',)
    list_display = ('__str__', 'title', 'date_added', 'date_modified',
                    'is_publicated', 'is_commentable', 'author')
    list_filter = ('is_publicated', 'date_added', 'author__username')
    search_fields = ['author__username']
    inlines = [CommentInline]


class CommentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'date_added', 'date_modified', 'is_publicated', 'author')
    list_filter = ('is_publicated', 'date_added', 'author__username')


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
