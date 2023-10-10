from rest_framework.permissions import BasePermission
from django.conf import settings


class IsTenantHandler(BasePermission):
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.username == settings.TENANT_HANDLER_USERNAME
    
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)