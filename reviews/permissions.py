from rest_framework import permissions


class ReviewPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if (request.method in permissions.SAFE_METHODS or
                request.user.is_authenticated):
            return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_anonymous:
            return False
        else:
            return bool(
                obj.author == request.user or
                request.user.role in ['admin', 'moderator'])


class CommentPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if (request.method in permissions.SAFE_METHODS or
                request.user.is_authenticated):
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            if request.method == "GET":
                return True
        else:
            return bool(
                obj.author == request.user or
                request.user.role in ['admin', 'moderator'])
