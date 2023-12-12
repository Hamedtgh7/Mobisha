from rest_framework.permissions import BasePermission


class Permission(BasePermission):
    def has_permission(self, request, view):
        if hasattr(request, 'allow') and getattr(request, 'allow') is not None:
            return True
        return False
