from rest_framework.permissions import BasePermission


class CheckoutPermission(BasePermission):
    
    def has_permission(self, request, view):
        return request.tenant.allow_purchase