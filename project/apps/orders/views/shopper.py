from utils.viewset import AtomicViewSet
from utils.decorators import get_queryset_wrapper
from ..serializers import OrderSerializer, OrderDetailedSerializer, OrderListSerializer
from ..models import Order, OrderProduct
from product.models import VariantAttribute
from django.db.models import Prefetch
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.generics import DestroyAPIView
from django.db.transaction import atomic

class OrderViewSet(AtomicViewSet, ReadOnlyModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer

    @get_queryset_wrapper
    def get_queryset(self):
        qs = super().get_queryset()
        if self.action == 'retrieve':
            qs = qs.prefetch_related(
            Prefetch(lookup='order_item_set', queryset=OrderProduct.objects.select_related('product_variant', 'product_variant__product')),
            Prefetch('order_item_set__product_variant__variant_attribute_set', VariantAttribute.objects.select_related('attribute')), 
            'order_item_set__product_variant__variant_image_set',
            'order_item_set__product_variant__product__name'
        ).select_related('shipment', 'shipment__phone_number')
        return qs.filter(shipment__user_id=self.request.user.id)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderDetailedSerializer            
        if self.request.method == 'POST':
            return OrderSerializer
        return super().get_serializer_class()


class CancelOrderView(DestroyAPIView):
    queryset = Order.objects.filter(payment_status = Order.PaymentStatus.PAID).prefetch_related(
        'payment_set'
    )
    
    @atomic()
    def perform_destroy(self, instance : Order):
        instance.cancel_order()

    @get_queryset_wrapper
    def get_queryset(self):
        qs = super().get_queryset()
        qs.filter(
            user=self.request.user
        )