from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Note, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    note = serializers.PrimaryKeyRelatedField(queryset=Note.objects.all())

    class Meta:
        model = Comment
        fields = ('id', 'author', 'note', 'text', 'created_at', 'updated_at', 'likes_count')
        read_only_fields = ('likes_count',)


class NoteSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Note
        fields = ('id', 'author', 'title', 'content', 'is_pinned', 'created_at', 'updated_at', 'likes_count', 'comments_count', 'comments')
        read_only_fields = ('likes_count',)

    def get_comments_count(self, obj):
        return obj.comments.count()
