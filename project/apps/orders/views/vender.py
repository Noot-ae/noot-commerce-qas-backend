from ..serializers import OrderProductSerializer
from ..models import OrderProduct
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.mixins import DestroyModelMixin
from utils.decorators import get_queryset_wrapper


class OrderProductViewSet(DestroyModelMixin, ReadOnlyModelViewSet):
    """This is just for vendor order"""
    queryset = OrderProduct.objects.select_related('product', 'product__product').prefetch_related('product__product__name').order_by('-order_id')
    serializer_class = OrderProductSerializer

    @get_queryset_wrapper
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(product_variant__product__user=self.request.user)