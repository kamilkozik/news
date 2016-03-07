from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, Textarea

from news.apps.news.models import Post, Comment


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'content')
        widgets = {
            'title': TextInput(attrs={'class': 'form-title'}),
            'content': Textarea(attrs={'class': 'form-content', 'cols': 80})
        }


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ('content',)


class UserForm(ModelForm):
    password = forms.PasswordInput(render_value=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
        widgets = {
            'password': forms.PasswordInput()
        }