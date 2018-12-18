from rest_framework import permissions


class IsOwnerOrAdminUserOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            if hasattr(obj, 'user'):
                return obj.user == request.user.id
            elif hasattr(obj, 'owner'):
                return obj.owner == request.user.id
            elif hasattr(obj, 'author'):
                return obj.author == request.user.id
            elif hasattr(obj, 'creator'):
                return obj.creator == request.user.id
            else:
                return request.user.id == obj.id or request.user.is_staff


class IsCurrentUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id

