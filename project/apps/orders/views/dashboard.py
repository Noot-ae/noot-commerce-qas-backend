from ..serializers import DashBoardOrderSerializer, DashBoardDetailedOrderSerializer, DashboardOrderCreateSerializer
from rest_framework.permissions import IsAdminUser
from ..filters import DashboardOrderFilter
from .shopper import OrderViewSet
from ..models import Order
from rest_framework.mixins import UpdateModelMixin

class DashBoardOrderViewSet(UpdateModelMixin, OrderViewSet):
    queryset = Order.objects.all()
    serializer_class = DashBoardOrderSerializer
    permission_classes = [IsAdminUser]
    filterset_class = DashboardOrderFilter

    def get_queryset(self):
        qs = super(OrderViewSet, self).get_queryset()
        if self.action == "retrieve":
            qs = OrderViewSet.queryset.select_related('shipment', 'shipment__phone_number')
        return qs

    def get_serializer_class(self, *args, **kwargs):
        if self.action == "retrieve":
            return DashBoardDetailedOrderSerializer
        if self.action == "create":
            return DashboardOrderCreateSerializer
        return super(OrderViewSet, self).get_serializer_class(*args, **kwargs)