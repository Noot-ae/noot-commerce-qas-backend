from rest_framework import serializers
from user.models import ShipmentProfile
from .vender import OrderProductSerializer
from utils.serializer_fields import CurrentUserRelatedField
from ..models import Order
from drf_writable_nested.serializers import WritableNestedModelSerializer
from utils.price_converter import get_active_currency_code

class OrderSerializer(WritableNestedModelSerializer):
    items = OrderProductSerializer(many=True, required=True, source="order_item_set")
    shipment = CurrentUserRelatedField(required=True, queryset = ShipmentProfile.objects.select_related('phone_number', 'region'), write_only=True)
    
    def create(self, validated_data):
        validated_data['order_currency_code'] = get_active_currency_code()
        order : Order = super().create(validated_data)
        order.set_total_prices()
        return order

    class Meta:
        model = Order
        fields = ('id', 'items', 'total_price', 'payment_status', 'shipment', 'order_status', 'created_at', 'order_notes', 'order_currency_code', 'shipping_price')
        extra_kwargs = {
            'payment_status' : {'read_only' : True},
            'order_status' : {'read_only' : True},
            'total_price' : {'read_only' : True},
            'order_currency_code' : {"read_only" : True},
            "shipping_price" : {"read_only" : True},
        }


class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'total_price', 'payment_status', 'shipment', 'order_status', 'created_at', 'order_notes')
