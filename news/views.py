from django.shortcuts import render
from django.views.generic.list import ListView

from news.models import Post


class PostList(ListView):
    model = Post
    context_object_name = 'post_list'

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        context['site_title'] = 'List of posts'
        return context
