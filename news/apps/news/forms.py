from django.contrib.auth.forms import UserCreationForm
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


# TODO(KK): Should be moved to person model directory
class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username',)
