from ..models import WishItem, Product, ProductVariant
from translations.serializers import TranslationSerializer
from rest_framework import serializers
from .variant import BaseVariantPriceMixin, ProductImageSerializer


class ProductWishSerializer(serializers.ModelSerializer):
    name = TranslationSerializer(many=True)
    
    class Meta:
        model = Product
        fields = ['id', 'display_image', 'slug', 'name']

    
class VariantWishSerializer(BaseVariantPriceMixin):
    image_set = ProductImageSerializer(required=False, many=True, source="variant_image_set")
    product = ProductWishSerializer()

    class Meta:
        model = ProductVariant
        fields = ['id', 'price', 'slug', 'image_set', 'product']


class WishItemSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = WishItem
        fields = ('id', 'product', 'created_at', 'user')
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['product'] = VariantWishSerializer(instance.product).data
        return data
    
