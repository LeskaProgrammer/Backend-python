from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Note, Comment, NoteLike, CommentLike
from .serializers import NoteSerializer, CommentSerializer, UserSerializer
from django.contrib.auth.models import User


class UserViewSet(viewsets.ModelViewSet):
    """CRUD для пользователей"""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class NoteViewSet(viewsets.ModelViewSet):
    """CRUD для заметок + лайки + закрепление"""
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'likes_count']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """Лайкнуть заметку"""
        note = self.get_object()
        like, created = NoteLike.objects.get_or_create(user=request.user, note=note)
        if created:
            note.likes_count += 1
            note.save()
            return Response({'status': 'liked', 'likes_count': note.likes_count})
        return Response({'status': 'already liked'}, status=400)

    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        """Убрать лайк"""
        note = self.get_object()
        try:
            like = NoteLike.objects.get(user=request.user, note=note)
            like.delete()
            note.likes_count = max(0, note.likes_count - 1)
            note.save()
            return Response({'status': 'unliked', 'likes_count': note.likes_count})
        except NoteLike.DoesNotExist:
            return Response({'status': 'not liked'}, status=400)

    @action(detail=True, methods=['post'])
    def pin(self, request, pk=None):
        """Закрепить заметку"""
        note = self.get_object()
        note.is_pinned = True
        note.save()
        return Response({'status': 'pinned'})

    @action(detail=True, methods=['post'])
    def unpin(self, request, pk=None):
        """Открепить заметку"""
        note = self.get_object()
        note.is_pinned = False
        note.save()
        return Response({'status': 'unpinned'})

    @action(detail=False, methods=['get'])
    def my(self, request):
        """Мои заметки"""
        notes = Note.objects.filter(author=request.user)
        serializer = self.get_serializer(notes, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    """CRUD для комментариев + лайки"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = Comment.objects.all()
        note_id = self.request.query_params.get('note')
        if note_id:
            queryset = queryset.filter(note_id=note_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """Лайкнуть комментарий"""
        comment = self.get_object()
        like, created = CommentLike.objects.get_or_create(user=request.user, comment=comment)
        if created:
            comment.likes_count += 1
            comment.save()
            return Response({'status': 'liked', 'likes_count': comment.likes_count})
        return Response({'status': 'already liked'}, status=400)

    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        """Убрать лайк"""
        comment = self.get_object()
        try:
            like = CommentLike.objects.get(user=request.user, comment=comment)
            like.delete()
            comment.likes_count = max(0, comment.likes_count - 1)
            comment.save()
            return Response({'status': 'unliked', 'likes_count': comment.likes_count})
        except CommentLike.DoesNotExist:
            return Response({'status': 'not liked'}, status=400)
