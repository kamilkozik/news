# -*- coding: utf8 -*-
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models.query import Prefetch
from django.shortcuts import render_to_response, redirect, render
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from news.apps.news.forms import PostForm, CommentForm, UserForm
from news.apps.news.models import Post, Comment


@method_decorator(login_required, name='dispatch')
class PostList(ListView):
    model = Post
    context_object_name = 'post_list'
    form = CommentForm()

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        context['site_title'] = 'List of posts'
        context['form'] = self.form
        return context

    def get_queryset(self):
        return super(PostList, self).get_queryset().prefetch_related(
            Prefetch('comments', queryset=Comment.objects.filter(is_authorized=True))).\
            filter(is_authorized=True)


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
class CommentCreate(CreateView):
    model = Comment
    fields = ['content']
    post_obj = None
    errors = u''
    form = CommentForm()

    def form_valid(self, form):
        if self.request.user.is_anonymous():
            self.errors = u'Aby dodawać komentarze musisz być zalogowany'
            return render_to_response('news/post_list.html',
                                      {'form': self.form,
                                       'errors': self.errors})

        post_pk = self.kwargs.get('post_pk', None)
        try:
            self.post_obj = Post.objects.get(pk=post_pk)
        except ObjectDoesNotExist:
            self.errors = u'Post nie istnieje'
            return render_to_response('news/post_list.html',
                                      {'form': self.form,
                                       'errors': self.errors})
        form.instance.author = self.request.user
        form.instance.post = self.post_obj
        return super(CommentCreate, self).form_valid(form)


def auth_view(request):
    form = AuthenticationForm()
    redirect_url = request.GET.get('next', None)
    context = RequestContext(request,
                             {'form': form,
                              'redirect_url': redirect_url})
    template = 'global/auth/login.html'
    return render_to_response(template_name=template, context=context)


def log_in(request):
    context = {}
    form = AuthenticationForm()
    user = authenticate(
        username=request.POST.get('username', None),
        password=request.POST.get('password', None)
    )

    if user is not None:
        if user.is_active:
            login(request, user)
            redirect_url = request.GET.get('redirect_url', False)
            if redirect_url:
                return redirect(redirect_url)
            return redirect(reverse('news:list'))
        else:
            context['errors'] = 'Account not activated'
            context['form'] = form
            return render(request, 'global/auth/login.html', context=context)
    else:
        context['errors'] = 'Pass or login wrong'
        context['form'] = form
        return render(request, 'global/auth/login.html', context=context)


def log_out(request):
    logout(request)
    return redirect(reverse('auth:show'))


def register_view(request):
    context = RequestContext(request)
    form = UserForm()
    context.push({'form': form})
    template = 'global/auth/register.html'
    return render(request, template_name=template, context=context)


def register(request):
    pass
