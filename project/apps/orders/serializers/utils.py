from .shopper import OrderSerializer
from user.serializers import ShipmentSerializer
from ..models import Order
from rest_framework import serializers

class OrderDetailedSerializer(OrderSerializer):
    shipment = ShipmentSerializer()


class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('order_status', 'order_notes')