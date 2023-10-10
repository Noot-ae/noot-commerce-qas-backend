from rest_framework.permissions import IsAuthenticated


class TranslationPermission(IsAuthenticated):
    
    def has_object_permission(self, request, view, obj):
        if request.method in view.SENSITIVE_METHODS:
            self.message = "you are not allowed to modify this object"
            return request.user.is_superuser or obj.is_user_owner
        return super().has_object_permission(request, view, obj)
