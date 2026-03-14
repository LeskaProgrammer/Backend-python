from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, NoteViewSet, CommentViewSet, NoteLikeViewSet, CommentLikeViewSet

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('notes', NoteViewSet)
router.register('comments', CommentViewSet)
router.register('note-likes', NoteLikeViewSet)
router.register('comment-likes', CommentLikeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
