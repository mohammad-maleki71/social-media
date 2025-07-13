from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages
from home.models import Post, Relation, Comment, Like
from .forms import PostUpdateCreateForm, CommentCreateForm, ReplyCreateForm, PostSearchForm
from django.utils.text import slugify
from account.models import User
from django.contrib.auth.mixins import LoginRequiredMixin



class HomeView(View):
    form_class = PostSearchForm
    def get(self, request):
        posts = Post.objects.all()
        if request.GET.get('search'):
            posts = posts.filter(content__icontains=request.GET['search'])
        return render(request, 'home/home.html', {'posts': posts, 'form': self.form_class})


class PostDetailsView(View):
    form_class = CommentCreateForm
    form_class_reply = ReplyCreateForm
    def setup(self, request, *args, **kwargs):
        self.post_instance = Post.objects.get(pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        comments = self.post_instance.pcomment.filter(is_reply=False)
        can_like = False
        if request.user.is_authenticated and self.post_instance.user_can_like(request.user):
            can_like = True
        return render(request, 'home/details.html', {'post': self.post_instance, 'comments': comments, 'form': self.form_class, 'form_reply': self.form_class_reply, 'can_like': can_like})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        comments = self.post_instance.pcomment.filter(is_reply=False)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.post_instance
            comment.user = request.user
            comment.save()
            messages.success(request, 'Comment saved','success')
            return redirect('home:details', self.post_instance.id)
        return render(request, 'home/details.html', {'post': self.post_instance, 'comments': comments, 'form': self.form_class})

class PostDeleteView(View):
    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)
        if request.user.id == post.user.id:
            post.delete()
            messages.success(request, 'Post deleted successfully', 'success')
            return redirect('account:profile', request.user.id)
        else:
            messages.error(request, 'You do not have permission to do that', 'danger')
            return redirect('home:home')

class PostUpdateView(View):
    form_class = PostUpdateCreateForm
    template_name = 'home/update.html'

    def setup(self, request, *args, **kwargs):
        self.post_instance = Post.objects.get(id=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = Post.objects.get(id=kwargs['post_id'])
        if not request.user.id == post.id:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(instance=post)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(request.POST, instance=post)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['content'][:30])
            new_post.save()
            messages.success(request, 'Post updated successfully', 'success')
            return redirect('home:details', new_post.id)
        return render(request, self.template_name, {'form': form})

class PostCreateView(View):
    form_class = PostUpdateCreateForm
    template_name = 'home/create.html'
    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            first_post = form.save(commit=False)
            first_post.user = request.user
            first_post.slug = slugify(form.cleaned_data['content'][:30])
            first_post.save()
            messages.success(request, 'Post created successfully', 'success')
            return redirect('home:details', first_post.id)
        return render(request, self.template_name, {'form': form})


class FollowView(LoginRequiredMixin,View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            messages.error(request, 'You do not have permission to do that', 'danger')
            return redirect('home:home')
        else:
            Relation.objects.create(from_user=request.user, to_user=user)
            messages.success(request, 'Follow successfully', 'success')
        return redirect('account:profile', user.id)

class UnFollowView(LoginRequiredMixin,View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            relation.delete()
            messages.success(request, 'Unfollow successfully', 'success')
        else:
            messages.error(request, 'You do not have permission to follow', 'danger')
        return redirect('account:profile', user.id)


class CommentReplyView(LoginRequiredMixin, View):
    def post(self, request, post_id, comment_id):
        form = ReplyCreateForm(request.POST)
        comment = Comment.objects.get(id=comment_id)
        post = Post.objects.get(id=post_id)
        if form.is_valid():
            new_reply = form.save(commit=False)
            new_reply.user = request.user
            new_reply.post = post
            new_reply.reply = comment
            new_reply.save()
            messages.success(request, 'you reply saved', 'success')
        return redirect('home:details', post.id)

class LikeView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)
        likes = Like.objects.filter(user=request.user, post=post)
        if likes.exists():
            messages.error(request, 'You already liked this post', 'danger')
        else:
            Like.objects.create(user=request.user, post=post)
            messages.success(request, 'You like successfully', 'success')
        return redirect('home:details', post.id)









