from django import forms
from django.views import View

from home.models import Post, Comment


class PostUpdateCreateForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'content', 'image']

class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class ReplyCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class PostSearchForm(forms.Form):
    search = forms.CharField()


