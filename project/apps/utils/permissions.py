from rest_framework.permissions import IsAdminUser, SAFE_METHODS

class IsAdminOrReadOnly(IsAdminUser):

    def has_permission(self, request, view):
        
        return bool(request.method in SAFE_METHODS or super().has_permission(request, view))
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return super().has_permission(request, view)