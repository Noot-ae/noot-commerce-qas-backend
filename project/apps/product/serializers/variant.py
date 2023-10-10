from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from ..models import ProductVariant, Attribute
from .attributes import AttributeValueSerializer
from .attributes import VariantAttributeSerializer
from .variant_image import ProductImageSerializer
from drf_writable_nested.serializers import WritableNestedModelSerializer
from translations.serializers import TranslationSerializer
from django.core.files.storage import default_storage


class BaseVariantPriceMixin(serializers.ModelSerializer):
    def to_representation(self, instance : ProductVariant):
        data = super().to_representation(instance)
        data['price'] = instance.get_exchanged_price()
        return data


class CartVariantSerializer(BaseVariantPriceMixin, serializers.ModelSerializer):
    images_set = ProductImageSerializer(required=False, many=True, source="variant_image_set")
    variant_attribute_set = VariantAttributeSerializer(many=True, read_only=True)

    class Meta:
        model = ProductVariant
        fields = ('id', 'variant_attribute_set', 'images_set', 'product', 'discount', 'price', 'quantity', 'slug')


class ProductVariantSerializer(BaseVariantPriceMixin, WritableNestedModelSerializer):
    variant_attribute_set = VariantAttributeSerializer(many=True, required=False)
    images_set = ProductImageSerializer(required=False, many=True, source="variant_image_set")

    class Meta:
        model = ProductVariant
        fields = ('id', 'variant_attribute_set', 'images_set', 'product', 'discount', 'price', 'quantity', 'slug', 'has_orders')
    
    def validate_product(self, product):
        if product.user_id != self.context['request'].user.id:
            raise ValidationError({"chosen product is not yours"}, code="invalid_product_choice")
        return product
    

class OverViewSearchProductVariantSerializer(BaseVariantPriceMixin, WritableNestedModelSerializer):
    display_image = serializers.SerializerMethodField()
    variant_attribute_set = VariantAttributeSerializer(many=True, required=False)

    def get_display_image(self, instance):
        # if instance.display_image is None: return
        return default_storage.url(instance.display_image)
    
    class Meta:
        model = ProductVariant
        fields = ('id', 'product', 'discount', 'price', 'quantity', 'slug', 'display_image', 'variant_attribute_set')


class OrderProductVariantSerializer(BaseVariantPriceMixin, WritableNestedModelSerializer):
    variant_attribute_set = VariantAttributeSerializer(many=True, required=False)
    images_set = ProductImageSerializer(required=False, many=True, source="variant_image_set")
    name = TranslationSerializer(source="product.name", many=True)

    
    class Meta:
        model = ProductVariant
        fields = ('id', 'variant_attribute_set', 'images_set', 'product', 'discount', 'price', 'quantity', 'slug', 'has_orders', 'name')


class SingleProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        exclude = ('product', 'slug')


class VarientAttributeSerializer(WritableNestedModelSerializer):
    attribute_value_set = AttributeValueSerializer(many=True, required=False)
    
    class Meta:
        model = Attribute
        fields = '__all__'
        
    def get_field_names(self, declared_fields, info):
        return super().get_field_names(declared_fields, info) + ["attribute_value_set"]
    
