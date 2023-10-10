from rest_framework.permissions import IsAuthenticated, SAFE_METHODS

class IsOwner(IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        is_auth = super().has_permission(request, view)
        return is_auth and obj.is_owner(request.user)