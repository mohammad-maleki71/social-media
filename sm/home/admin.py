from django.contrib import admin
from .models import Post, Relation, Comment, Like


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'created')
    list_filter = ('created',)
    search_fields = ('title',)
    raw_id_fields = ('user',)

admin.site.register(Relation)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created', 'is_reply')
    list_filter = ('created',)
    search_fields = ('content',)
    raw_id_fields = ('user','post', 'reply')

admin.site.register(Like)