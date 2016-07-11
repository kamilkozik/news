# -*- coding: utf8 -*-

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseBadRequest
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.utils.decorators import method_decorator
from django.views.generic import CreateView
from django.views.generic.edit import DeleteView
from news.apps.news.forms import CommentForm
from news.apps.news.models import Comment, Post


# # # # # # # # # # # #
# Comment related views
#
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


