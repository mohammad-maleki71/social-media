from django.db import models
from account.models import User


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    slug = models.SlugField(max_length=200)
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/%Y/%m/%d')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']

    def user_can_like(self, user):
        user_like = user.ulike.filter(post=self)
        if user_like.exists():
            return True
        return False

class Relation(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='frelations')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trelations')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.from_user} follow {self.to_user}'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='pcomment')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ucomment')
    is_reply = models.BooleanField(default=False)
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='rcomment', null=True, blank=True)
    content = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} {self.content[:20]}'


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='plike')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ulike')

    def __str__(self):
        return f'{self.user} liked {self.post}'








