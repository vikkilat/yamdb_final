from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Настройка доступа для вьюсетов - админ или только чтение."""
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated
            and (request.user.is_admin or request.user.is_superuser)
        )


class IsAdmin(permissions.BasePermission):
    """Настройка доступа - админ."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser
        )


class IsAdminModeratorAuthorOrReadOnly(permissions.BasePermission):
    """Доступ к контенту доступен только автору, админу, модератору."""
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
            or request.user.is_moderator
            or obj.author == request.user
        )
