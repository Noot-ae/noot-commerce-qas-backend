from drf_writable_nested import WritableNestedModelSerializer
from ..models import Order
from .shopper import OrderProductSerializer
from user.serializers import GuestShipmentSerializer


class GuestOrderSerializer(WritableNestedModelSerializer):
    items = OrderProductSerializer(many=True, required=True, source="order_item_set")
    shipment = GuestShipmentSerializer()
    

    class Meta:
        read_only_fields = ['total_price', 'order_status', 'shipping_price', 'payment_status', 'order_currency_code']
        model = Order
        fields = '__all__'
        extra_kwargs = {key : {"read_only" : True} for key in read_only_fields}