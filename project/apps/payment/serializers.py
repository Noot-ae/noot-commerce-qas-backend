from rest_framework import serializers
from .models import Payment
from orders.models import Order, OrderProduct
from django.db.models import Prefetch, Exists, Subquery, OuterRef
from user.models import ShipmentProfile
from utils.serializer_fields import CurrentUserRelatedField
from orders.exceptions import OrderSoldException

class ValidateOrderMixin:
    def validate_order(self, order : Order):
        if order.is_already_paid:
            raise OrderSoldException()
        order.validate()
        return order


class PaymentSerializer(ValidateOrderMixin, serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    order = CurrentUserRelatedField(queryset=Order.objects.annotate(
                is_already_paid = Exists(Subquery(Payment.objects.filter(order_id = OuterRef("pk"))))
        ).prefetch_related(Prefetch('order_item_set', OrderProduct.objects.select_related('product_variant'))))

    class Meta:
        model = Payment
        fields = '__all__'
        extra_kwargs = {
            'paid_amount' : {'read_only' : True}
        }
            
        
class PaymobPaySerializer(ValidateOrderMixin, serializers.Serializer):
    
    order = CurrentUserRelatedField(queryset=Order.objects.annotate(
                is_already_paid = Exists(Subquery(Payment.objects.filter(order_id = OuterRef("pk"))))
        ).prefetch_related(Prefetch('order_item_set', OrderProduct.objects.select_related('product_variant'))))
    
    profile = CurrentUserRelatedField(queryset=ShipmentProfile.objects.select_related('phone_number'))

    @property
    def validated_data(self):
        from orders.serializers import OrderProductListSerializer
        data = super().validated_data
        data['serialized_order_items'] = OrderProductListSerializer(data['order'].order_item_set.all(), many=True).data
        return data
    
    
