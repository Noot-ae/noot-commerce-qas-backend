from utils.cache import get_best_seller_sold_amount
from utils.decorators import get_queryset_wrapper
from ..serializers import ProductSerializer, ProductUpdateSerializer, ProductDisplaySerializer
from ..models import Product, ProductVariant, VariantAttribute
from utils.viewset import AtomicViewSet
from django.db.models import Prefetch, Exists, Subquery, OuterRef, Count, Avg, When, Case, BooleanField
from orders.models import OrderProduct
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.generics import UpdateAPIView
from rest_framework.mixins import DestroyModelMixin
from ..filters import ProductFilterSet
from utils.mixins import CacheResponseMixin
# Create your views here.

class ProductsView(CacheResponseMixin, ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_online=True).prefetch_related('name', 'description', 'category')
    serializer_class = ProductDisplaySerializer
    permission_classes = ()
    authentication_classes = ()
    filterset_class = ProductFilterSet
    lookup_field = "slug"
    lookup_url_kwarg = "slug"
    
    def get_queryset(self):
        qs = self.queryset
        
        first_variant_price_subquery = ProductVariant.objects.filter(
            product__pk=OuterRef('pk')
        ).order_by('id').values('price')[:1]

        first_variant_id_subquery = ProductVariant.objects.filter(
            product__pk=OuterRef('pk')
        ).order_by('id').values('id')[:1]

        first_variant_quantity_subquery = ProductVariant.objects.filter(
            product__pk=OuterRef('pk')
        ).order_by('id').values('quantity')[:1]

        first_variant_discount_subquery = ProductVariant.objects.filter(
            product__pk=OuterRef('pk')
        ).order_by('id').values('discount')[:1]

        third_top_best_seller = get_best_seller_sold_amount()

        if self.action == "retrieve":            
            qs = qs.prefetch_related(Prefetch('product_variant_set', queryset=ProductVariant.objects.annotate(
                    _has_orders = Exists(
                        Subquery(
                            OrderProduct.objects.filter(product_variant__product = OuterRef("pk"))
                        )
                    )
                ).prefetch_related(
                    Prefetch('variant_attribute_set', queryset=VariantAttribute.objects.select_related("attribute", "value")), 'variant_image_set'
            )))
            
        qs = qs\
            .annotate(
                first_variant_id = Subquery(first_variant_id_subquery),
                stock = Subquery(first_variant_quantity_subquery), 
                total_rating = Avg('productrating__rate'),
                price = Subquery(first_variant_price_subquery),
                discount = Subquery(first_variant_discount_subquery),
                amount_sold = Count('product_variant_set__as_order_item_set__quantity'),
                is_best_seller = Case(
                    When(
                        amount_sold__gte = third_top_best_seller, then=True,
                    ), 
                    output_field=BooleanField(), default= False
                )
            )
            
        return qs
    
    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProductSerializer
        return super().get_serializer_class()


class MyProductsView(ProductsView):
    @get_queryset_wrapper
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)


class ProductCreateView(AtomicViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class UpdateDeleteProductView(DestroyModelMixin, UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductUpdateSerializer

    @get_queryset_wrapper
    def get_queryset(self):
        if self.request.user.is_staff:
            return super().get_queryset()
        return super().get_queryset().filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)



    
