from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # write permissions are only allowed to the owner
        return obj.owner == request.user.player
    
class IsRelatedPlayerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # write permissions are only allowed to the owner
        return obj.player == request.user.player