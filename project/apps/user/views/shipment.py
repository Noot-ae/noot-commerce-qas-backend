from ..models import ShipmentProfile
from ..serializers import ShipmentSerializer, DashboardShipmentSerializer, OverViewShipmentSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView
from ..filters import ProfileFilter
from rest_framework.permissions import IsAdminUser, DjangoModelPermissions


class OverViewShipmentView(ListCreateAPIView):
    queryset = ShipmentProfile.objects.all()
    filterset_class = ProfileFilter
    permission_classes = [IsAdminUser | DjangoModelPermissions]
    serializer_class = OverViewShipmentSerializer


class ShipmentViewSet(ModelViewSet):
    queryset = ShipmentProfile.objects.select_related('phone_number').all()
    serializer_class = ShipmentSerializer
    filterset_fields = ['user_id', 'region', 'phone_number']
    
    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return DashboardShipmentSerializer
        return super().get_serializer_class()
    
    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_superuser:
            return qs        
        if self.request.user.is_authenticated:                    
            qs = qs.filter(user=self.request.user)
        return qs
    
