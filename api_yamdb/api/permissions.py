from rest_framework import permissions

from users.models import User


class IsAuthorModeratorAdminOrReadOnly(permissions.BasePermission):
    """
    Автор объекта - может редактировать и удалять свои отзывы и комментарии,
    редактировать свои оценки произведений.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (obj.author == request.user
                or request.user.role == User.UserRoles.ADMIN
                or request.user.role == User.UserRoles.MODERATOR)


class IsAdmin(permissions.BasePermission):
    """
    Администратор (admin) или суперюзер (is_superuser) — полные права на
    управление всем контентом проекта. Может создавать и удалять произведения,
    категории и жанры. Может назначать роли пользователям.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.is_superuser
                 or request.user.role == User.UserRoles.ADMIN)
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and (request.user.is_superuser
                 or request.user.role == User.UserRoles.ADMIN)
        )


class IsAdminOrGetList(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in 'list':
            return True
        if view.action == 'create' or 'destroy':
            return (
                request.user.is_authenticated
                and (request.user.is_superuser
                     or request.user.role == User.UserRoles.ADMIN)
            )

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return False
        return (
            request.user.is_authenticated
            and (request.user.is_superuser
                 or request.user.role == User.UserRoles.ADMIN)
        )


class IsAdminOrRead(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'list':
            return True
        if view.action == 'retrieve':
            return True
        if view.action == 'create' or 'destroy' or 'update':
            return (
                request.user.is_authenticated
                and (request.user.is_superuser
                     or request.user.role == User.UserRoles.ADMIN)
            )

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return True
        return (
            request.user.is_authenticated
            and (request.user.is_superuser
                 or request.user.role == User.UserRoles.ADMIN)
        )
