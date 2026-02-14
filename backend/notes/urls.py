from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, NoteViewSet, CommentViewSet

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('notes', NoteViewSet)
router.register('comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
