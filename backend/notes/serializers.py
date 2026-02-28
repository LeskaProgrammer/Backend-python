from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Note, Comment, NoteLike, CommentLike


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class NoteLikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = NoteLike
        fields = ('id', 'user', 'note')
        read_only_fields = ('user',)


class CommentLikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = CommentLike
        fields = ('id', 'user', 'comment')
        read_only_fields = ('user',)


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


class NoteLightSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Note
        fields = ('id', 'author_username', 'title', 'is_pinned', 'created_at', 'likes_count')


class CommentLightSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    note_title = serializers.CharField(source='note.title', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'author_username', 'note_title', 'text', 'created_at', 'likes_count')
