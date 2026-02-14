from django.contrib import admin
from .models import Note, Comment, NoteLike, CommentLike


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_pinned', 'likes_count', 'created_at')
    list_filter = ('is_pinned', 'created_at', 'author')
    search_fields = ('title', 'content')
    date_hierarchy = 'created_at'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'note', 'likes_count', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('text',)


@admin.register(NoteLike)
class NoteLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'note')
    list_filter = ('user',)


@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment')
    list_filter = ('user',)
