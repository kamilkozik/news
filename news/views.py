# -*- coding: utf8 -*-
from django.shortcuts import render_to_response
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from news.forms import PostForm
from news.models import Post


class PostList(ListView):
    model = Post
    context_object_name = 'post_list'
    form = PostForm()

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        context['site_title'] = 'List of posts'
        context['form'] = self.form
        return context

    def get_queryset(self):
        return super(PostList, self).get_queryset().prefetch_related('comments')


class PostCreate(CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        if self.request.user.is_anonymous():
            form = PostForm()
            errors = u'Aby dodać post musisz być zalogownay'
            return render_to_response('news/post_form.html',
                                      {'form': form, 'errors': errors})
        form.instance.author = self.request.user
        return super(PostCreate, self).form_valid(form)
