from product.serializers import  ProductUpdateSerializer, OverViewProductSerachSerializer
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from .mixins import BaseViewMixin
from product.views import ProductsView
from rest_framework.generics import ListAPIView
from product.models import Product, ProductVariant, ProductDescription, ProductImage, VariantAttribute
from django.db.models import Count, OuterRef, Subquery, Avg
from ..serializers import ProductTopSerializer
from rest_framework.settings import api_settings
from django.db.models import Prefetch
from product.serializers import ProductRetrieveOverViewSerializer
from rest_framework.viewsets import GenericViewSet


class ProductViewSet(BaseViewMixin, DestroyModelMixin, UpdateModelMixin, ProductsView):
    lookup_field = "pk"
    lookup_url_kwarg = "pk"
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES
    
    def dispatch(self, *args, **kwargs): 
        return GenericViewSet.dispatch(self, *args, **kwargs)

    @property
    def is_retrieve(self):
        return self.action == 'retrieve'

    @property
    def is_search(self):
        return self.request.GET.get('content')

    def get_queryset(self):
        if self.is_search and not self.is_retrieve:
            variant_first_image_subquery = ProductImage.objects.filter(
                product_variant_id = OuterRef('pk')
            ).order_by('id').values('image')[:1]
            
            full_product_prefetch_query = Prefetch(
                'product_variant_set', 
                queryset=ProductVariant.objects.annotate(
                    display_image = Subquery(variant_first_image_subquery)
                ).prefetch_related(
                    'variant_image_set',
                    Prefetch(
                        'variant_attribute_set', 
                        queryset=VariantAttribute.objects.select_related("attribute", "value")
                    )
                )
            )
            qs = Product.objects.filter(is_online=True)\
                .prefetch_related('name', 'description', full_product_prefetch_query)\
                .distinct('id').order_by('id')
            return qs

        qs = super().get_queryset()
        if self.is_retrieve:
            qs = qs.prefetch_related(
                Prefetch(
                    "product_description_set", 
                    queryset=ProductDescription.objects.filter(is_active=True).prefetch_related("name", "description")
                )
            )
        return qs

    def get_serializer_class(self):
        if self.is_search:
            return OverViewProductSerachSerializer
        elif self.is_retrieve:
            return ProductRetrieveOverViewSerializer
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.serializer_class = ProductUpdateSerializer
        return super().get_serializer_class()


class TopProductsView(ListAPIView):    
    first_variant_price_subquery = ProductVariant.objects.filter(
        product__pk=OuterRef('pk')
    ).order_by('id').values('price')[:1]

    queryset =  Product.objects.annotate(
                amount_sold = Count('product_variant_set__as_order_item_set__quantity'),
                rate = Avg("productrating"),
                price = Subquery(first_variant_price_subquery)
    ).order_by('-amount_sold').prefetch_related("name")
    serializer_class = ProductTopSerializer
    permission_classes = []
    authentication_classes = []