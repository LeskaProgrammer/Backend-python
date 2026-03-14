from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrReadOnly(BasePermission):
    """Разрешает изменять/удалять объект только его автору."""

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return getattr(obj, 'author_id', None) == request.user.id


class IsSelfOrReadOnly(BasePermission):
    """Пользователь может изменять только свой профиль."""

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff or obj.id == request.user.id
