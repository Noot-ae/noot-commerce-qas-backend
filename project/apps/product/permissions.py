from rest_framework.permissions import BasePermission

class VariantDeletePermission(BasePermission):
    message = "can't delete variant with existing orders"
    
    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':                
            return (not obj.has_orders)
        return True
