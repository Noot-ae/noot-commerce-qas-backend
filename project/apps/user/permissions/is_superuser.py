from rest_framework.permissions import IsAuthenticated

class IsSuperuser(IsAuthenticated):

    def has_permission(self, request, view):
        is_logged = super().has_permission(request, view) 
        return is_logged and request.user.is_superuser