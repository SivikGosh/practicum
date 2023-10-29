from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrReadOnlyPermission(BasePermission):
    """изменение или удаление поста только автором, инача рид онли"""
    def has_permission(self, request, view):
        # оставляю доступ только аутентифицированным, согласно ТЗ
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in ('PUT', 'PATCH', 'DELETE'):
            return obj.author == request.user
        return request.method in SAFE_METHODS
