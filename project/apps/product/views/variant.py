from utils.decorators import get_queryset_wrapper
from ..serializers import SingleProductVariantSerializer, ProductVariantSerializer
from ..models import ProductVariant
from rest_framework.viewsets import ModelViewSet
from django.db.models import Exists, Subquery, OuterRef
from orders.models import OrderProduct
from rest_framework.permissions import IsAdminUser
from user.permissions import IsVender
from ..permissions import VariantDeletePermission


class ProductVariantViewSet(ModelViewSet):
    queryset = ProductVariant.objects.all()
    permission_classes = (IsAdminUser | IsVender, VariantDeletePermission)
    filterset_fields = ('product',)
    
    @get_queryset_wrapper
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == "destroy":                
            queryset = queryset\
            .annotate(_has_orders=Exists(Subquery(OrderProduct.objects.filter(product_variant = OuterRef("pk")))))
            
        elif self.request.method == 'get':
            queryset = queryset.prefetch_related('images_set', 'variant_attribute_set')
        elif self.action in ['update', 'partial_update']:
            queryset = queryset.filter(product__user=self.request.user)
        return queryset

    
    def get_permissions(self):
        if self.request.method == 'GET':
            return []
        return super().get_permissions()
    
    def get_serializer_class(self):
        method = self.request.method
        if method == "POST" or method == 'GET':
            return ProductVariantSerializer
        else:
            return SingleProductVariantSerializer
