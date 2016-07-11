# -*- coding: utf8 -*-

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy, reverse
from django.db.models import Prefetch
from django.http import HttpResponseBadRequest
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView
from news.apps.news.forms import CommentForm, PostForm
from news.apps.news.models import Post, Comment


# # # # # # # # # # # #
# Post related views


@method_decorator(login_required, name='dispatch')
class PostList(ListView):
    model = Post
    context_object_name = 'post_list'
    form = CommentForm()

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()

        if context.get('post_list', False):
            posts_form_obj_list = []
            posts = context.get('post_list', None)
            for post in posts:
                posts_form_obj_list.append(
                    {
                        'post': post,
                        'form_post': PostForm(initial={'title': post.title, 'content': post.content})
                    }
                )

            context.update(
                {'site_title': 'List of posts', 'form': self.form, 'post_list': posts_form_obj_list}
            )
        return context

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return super(PostList, self).get_queryset().\
                prefetch_related(Prefetch('comments', queryset=Comment.objects.all()))
        return super(PostList, self).get_queryset().\
            prefetch_related(Prefetch('comments', queryset=Comment.objects.filter(is_publicated=True))).\
            filter(is_publicated=True)


@method_decorator(login_required, name='dispatch')
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


@method_decorator(login_required, name='dispatch')
class PostDelete(DeleteView):
    model = Post
    success_url = reverse_lazy('news:list')


def post_update(request, pk):
    user = request.user
    form = PostForm(request.POST)
    if form.is_valid():
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return HttpResponseBadRequest()

        if post.author == user:
            post.title = form.cleaned_data['title']
            post.content = form.cleaned_data['content']
            post.save()
            return HttpResponseRedirect(reverse('news:list'))
    return HttpResponseBadRequest()


def post_publish(request, post_pk):
    user = request.user
    if not user.is_staff:
        return HttpResponseBadRequest()
    try:
        post = Post.objects.get(pk=post_pk)
    except Post.DoesNotExist:
        return HttpResponseBadRequest()
    post.publish_post()
    post.save()
    return HttpResponseRedirect(reverse('news:list'))
