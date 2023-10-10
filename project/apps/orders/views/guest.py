from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from ..models import Order
from ..serializers import GuestOrderSerializer

class GuestOrderViewSet(CreateModelMixin, GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = GuestOrderSerializer
    permission_classes = []
    authentication_classes = []
    