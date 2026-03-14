from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Count
from .models import Note, Comment, NoteLike, CommentLike
from .serializers import (
    NoteSerializer, CommentSerializer, UserSerializer,
    NoteLikeSerializer, CommentLikeSerializer,
    NoteLightSerializer, CommentLightSerializer
)
from .permissions import IsAuthorOrReadOnly, IsSelfOrReadOnly
from django.contrib.auth.models import User


class UserViewSet(viewsets.ModelViewSet):
    """CRUD для пользователей"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsSelfOrReadOnly]
    
    @action(detail=False, methods=['get'])
    def top_by_notes(self, request):
        """Топ пользователей по количеству заметок"""
        limit = int(request.query_params.get('limit', 10))
        users = User.objects.annotate(
            notes_count=Count('notes')
        ).filter(notes_count__gt=0).order_by('-notes_count')[:limit]
        
        data = [
            {
                'id': user.id,
                'username': user.username,
                'notes_count': user.notes_count
            }
            for user in users
        ]
        return Response(data)
    
    @action(detail=False, methods=['get'])
    def top_by_comments(self, request):
        """Топ пользователей по количеству комментариев"""
        limit = int(request.query_params.get('limit', 10))
        users = User.objects.annotate(
            comments_count=Count('comments')
        ).filter(comments_count__gt=0).order_by('-comments_count')[:limit]
        
        data = [
            {
                'id': user.id,
                'username': user.username,
                'comments_count': user.comments_count
            }
            for user in users
        ]
        return Response(data)


class NoteViewSet(viewsets.ModelViewSet):
    """CRUD для заметок + лайки + закрепление"""
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
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
    
    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Популярные заметки (по количеству лайков)"""
        limit = int(request.query_params.get('limit', 10))
        notes = Note.objects.filter(likes_count__gt=0).order_by('-likes_count')[:limit]
        serializer = NoteLightSerializer(notes, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pinned(self, request):
        """Закрепленные заметки"""
        notes = Note.objects.filter(is_pinned=True).order_by('-created_at')
        serializer = NoteLightSerializer(notes, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Статистика по заметкам"""
        total_notes = Note.objects.count()
        pinned_notes = Note.objects.filter(is_pinned=True).count()
        total_likes = Note.objects.aggregate(total=Count('notelike'))['total'] or 0
        
        # Самая популярная заметка
        most_liked = Note.objects.order_by('-likes_count').first()
        most_liked_data = None
        if most_liked:
            most_liked_data = {
                'id': most_liked.id,
                'title': most_liked.title,
                'likes_count': most_liked.likes_count
            }
        
        return Response({
            'total_notes': total_notes,
            'pinned_notes': pinned_notes,
            'total_likes': total_likes,
            'most_liked_note': most_liked_data
        })
    
    @action(detail=False, methods=['get'])
    def lightweight(self, request):
        """Легковесный список заметок (без комментариев)"""
        notes = self.filter_queryset(self.get_queryset())
        serializer = NoteLightSerializer(notes, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    """CRUD для комментариев + лайки"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

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
    
    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Популярные комментарии (по количеству лайков)"""
        limit = int(request.query_params.get('limit', 10))
        comments = Comment.objects.filter(likes_count__gt=0).order_by('-likes_count')[:limit]
        serializer = CommentLightSerializer(comments, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_author(self, request):
        """Комментарии конкретного автора"""
        author_id = request.query_params.get('author_id')
        if not author_id:
            return Response({'error': 'author_id parameter is required'}, status=400)
        
        comments = Comment.objects.filter(author_id=author_id).order_by('-created_at')
        serializer = CommentLightSerializer(comments, many=True)
        return Response(serializer.data)


class NoteLikeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NoteLike.objects.all()
    serializer_class = NoteLikeSerializer


class CommentLikeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeSerializer
