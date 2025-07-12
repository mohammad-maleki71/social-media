from django.contrib import admin
from .models import Post, Relation


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'created')
    list_filter = ('created',)
    search_fields = ('title',)
    raw_id_fields = ('user',)

admin.site.register(Relation)