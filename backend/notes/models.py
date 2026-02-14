from django.db import models
from django.contrib.auth.models import User


class Note(models.Model):
    """Заметка пользователя"""
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержимое')
    is_pinned = models.BooleanField(default=False, verbose_name='Закреплена')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['-is_pinned', '-created_at']
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Комментарий к заметке"""
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f"Комментарий от {self.author.username}"


class NoteLike(models.Model):
    """Лайк заметки"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('user', 'note')


class CommentLike(models.Model):
    """Лайк комментария"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('user', 'comment')
