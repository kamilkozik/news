from django.forms import ModelForm

from news.models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
