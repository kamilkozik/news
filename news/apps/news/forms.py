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
