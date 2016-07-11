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


def homepage(request):
    # Get all posts
    pass


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
