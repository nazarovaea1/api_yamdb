from rest_framework import permissions
from rest_framework.permissions import IsAdminUser

from api_auth.models import ROLE_CHOICES


class IsAdminUserOrReadOnly(IsAdminUser):
    def has_permission(self, request, view):
        # is_admin = super(
        #     IsAdminUserOrReadOnly,
        #     self).has_permission(request, view)
        is_admin = super().has_permission(request, view)
        return request.method in permissions.SAFE_METHODS or is_admin


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user or request.user.role in ROLE_CHOICES
