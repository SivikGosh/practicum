from rest_framework import permissions


class IsAuthenticatedAdmin(permissions.BasePermission):
    """Разрешение 'Если_Пользователь_Администратор'."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser
        )


class IsAuthorOrHiAccessOrReadOnly(permissions.BasePermission):
    """Разрешение 'Если_Пользователь_Автор_Или_Его_Роль_Разрешена'."""

    message = 'Изменение чужого контента запрещено!'

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.is_admin
                or request.user.is_moderator
                or request.user.is_superuser)


class IsAdminOrReadOnly(permissions.BasePermission):
    """Разрешение 'Если_Пользователь_Администратор'."""

    message = 'Изменение чужого контента запрещено!'

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
            or request.user.is_superuser
        )
