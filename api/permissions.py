from rest_framework import permissions


class IsOwnerOrAdminUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or request.user.is_staff


class IsOwnerOrAdminUserOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or request.user.is_staff
