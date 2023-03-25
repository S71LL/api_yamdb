from rest_framework import permissions


class AuthorOrReadOnly(permissions.BasePermission):
    """
    Автор объекта - может редактировать и удалять свои отзывы и комментарии,
    редактировать свои оценки произведений.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user and request.user.is_authenticated


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
                 or request.user.role == 'admin')
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and (request.user.is_superuser
                 or request.user.role == 'admin')
        )


class IsModerator(permissions.BasePermission):
    """
    Модератор (moderator) — те же права, что и у Аутентифицированного
    пользователя, плюс право удалять и редактировать
    любые отзывы и комментарии.
    """

    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated
                and request.user.role == 'moderator')


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Изменения может привносить только Администратор,
    чтение доступно для всех
    """

    def has_permission(self, request, view):
        if view.action == 'list':
            return True

        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated and request.user.is_admin
        )

    def has_object_permission(self, request, view, obj):

        if view.action == 'destroy' or 'create':
            return request.user.is_authenticated and (
                request.user.role == 'admin' or request.user.is_superuser
            )


class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Доступ на чтение имеют все.
    На изменение только админ и модератор
    """

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.role == 'admin')
                )

    def has_object_permission(self, request, view, obj):
        return (request.method == 'GET'
                or request.user.is_authenticated
                and (request.user.is_superuser
                     or request.user.role == 'admin')
                )
