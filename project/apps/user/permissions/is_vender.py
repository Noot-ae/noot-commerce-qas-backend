from vender.models import Vender
from rest_framework.permissions import IsAuthenticated

class IsVender(IsAuthenticated):

    def has_permission(self, request, view):
        is_logged = super().has_permission(request, view) 
        return is_logged and Vender.objects.filter(user=request.user).exists()