from rest_framework.viewsets import ModelViewSet
from ..models import CartItem
from ..serializers import CartItemSerializer
from utils.decorators import get_queryset_wrapper

class CartViewSet(ModelViewSet):
    queryset = CartItem.objects.all().select_related('product', 'product__product').prefetch_related(
        'product__variant_attribute_set', 
        'product__variant_image_set',
        'product__product__name'
    )
    serializer_class = CartItemSerializer
    
    @get_queryset_wrapper
    def get_queryset(self):
        return super().get_queryset().filter(user =self.request.user)