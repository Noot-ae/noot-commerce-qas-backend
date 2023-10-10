from ..serializers import UserPhoneSerializer, PhoneDashboardSerializer
from ..models import UserPhone
from rest_framework.viewsets import ModelViewSet
from utils.decorators import get_queryset_wrapper

class UserPhoneViewSet(ModelViewSet):
    queryset = UserPhone.objects.all()
    serializer_class = UserPhoneSerializer
    lookup_field = "phone"
    lookup_url_kwarg = "phone"
    
    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return PhoneDashboardSerializer
        return super().get_serializer_class()
    
    @get_queryset_wrapper
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs