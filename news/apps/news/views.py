# -*- coding: utf8 -*-
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models.query import Prefetch
from django.forms import forms
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render_to_response, redirect, render
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from news.apps.news.forms import PostForm, CommentForm, UserForm
from news.apps.news.models import Post, Comment


# # # # # # # # # # # #
# Post related views
from news.apps.person.models import Person


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


# # # # # # # # # # # #
# Comment related views

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


@method_decorator(login_required, name='dispatch')
class CommentDelete(DeleteView):
    model = Comment
    success_url = reverse_lazy('news:list')


def comment_publish(request, comment_pk):
    user = request.user
    if not user.is_staff:
        return HttpResponseBadRequest()
    try:
        comment = Comment.objects.get(pk=comment_pk)
    except Comment.DoesNotExist:
        return HttpResponseBadRequest()
    comment.publish_comment()
    comment.save()
    return HttpResponseRedirect(reverse('news:list'))


# # # # # # # # # # # #
# Auth related views

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
                return HttpResponseRedirect(redirect_url)
            return HttpResponseRedirect(reverse('news:list'))
        else:
            context['errors'] = 'Account not activated'
            context['form'] = form
            if hasattr(request.session, 'inactive_user_login_count'):
                request.session['inactive_user_login_count'] += 1
            else:
                request.session['inactive_user_login_count'] = 1
            return render(request, 'global/auth/login.html', context=context)
    else:
        if hasattr(request.session, 'bad_login'):
            request.session['bad_login'] += 1
        else:
            request.session['bad_login'] = 1
        context['errors'] = 'Pass or login wrong'
        context['form'] = form
        return render(request, 'global/auth/login.html', context=context)


def log_out(request):
    print getattr(request, 'user')
    logout(request)
    print getattr(request, 'user')
    return redirect(reverse('news:list'))


def register_view(request):
    context = RequestContext(request)
    form = UserForm()
    context.push({'form': form})
    template = 'global/auth/register.html'
    return render(request, template_name=template, context=context)


def register(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        try:
            form.clean_password2()
        except forms.ValidationError:
            form = UserCreationForm()
            return render(request, 'global/auth/register.html', context={'form': form})
        form.save()
        try:
            user = User.objects.get(username=form.cleaned_data.get('username'))
        except User.DoesNotExist:
            return render(request, 'global/auth/register.html', context={'form': form})

        if user:
            person = Person(user=user)
            person.save()
        return redirect('auth:show')
    form = UserCreationForm()
    return render(request, 'global/auth/register.html', context={'form': form})



# # # # # # # # # # # #
# Session related views

@login_required
def flush_session_values(request):
    for key, value in request.session.items():
        print key, value
    request.session.clear()
    return HttpResponse('Session\'s clean method used')
