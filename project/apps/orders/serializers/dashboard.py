from .shopper import OrderSerializer
from user.serializers import ShipmentSerializer
from rest_framework import serializers
from ..models import Order
from user.models import ShipmentProfile


class DashBoardOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'payment_status', 'order_status', 'created_at', 'total_price', 'order_notes')
        

class DashBoardDetailedOrderSerializer(OrderSerializer):
    shipment = ShipmentSerializer()
    

class DashboardOrderCreateSerializer(OrderSerializer):
    shipment = serializers.PrimaryKeyRelatedField(required=True, queryset = ShipmentProfile.objects.select_related('phone_number', 'region'), write_only=True)

    class Meta(OrderSerializer.Meta):
        extra_kwargs = {
            'total_price' : {'required' : False},
            'order_currency_code' : {"read_only" : True},
            "shipping_price" : {"required" : False},
        }
