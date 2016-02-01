# -*- coding: utf8 -*-

from django.contrib import admin

from news.models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    pass


class CommentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
