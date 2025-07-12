from django import forms
from django.views import View

from home.models import Post


class PostUpdateCreateForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'content', 'image']


