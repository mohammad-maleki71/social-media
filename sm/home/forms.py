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
    search = forms.CharField(label=False, widget=forms.TextInput(attrs={'class': 'block w-full p-2 ps-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'}))


