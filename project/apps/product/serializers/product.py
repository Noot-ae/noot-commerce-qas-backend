from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from ..models import Product
from translations.serializers import TranslationSerializer
from .variant import ProductVariantSerializer, OverViewSearchProductVariantSerializer
from drf_writable_nested.mixins import NestedCreateMixin
from category.models import Category
from .description import ProductDescriptionSerializer
from utils.price_converter import price_converter

update_list_of_dicts = lambda l, key, value: [ dict(**i, **{key : value}) for i in l]


class BaseProductDisplaySerializer(serializers.ModelSerializer):
    price = serializers.IntegerField(read_only=True)
    first_variant_id = serializers.IntegerField(read_only=True)
    price = serializers.IntegerField(read_only=True)
    stock = serializers.IntegerField(read_only=True)
    discount = serializers.IntegerField(read_only=True)
    rate = serializers.IntegerField(read_only=True, source="total_rating")
    name = TranslationSerializer(many=True, required=True)
    description = TranslationSerializer(many=True, required=False)
    slug = serializers.CharField(read_only=True)
    is_best_seller = serializers.BooleanField(read_only=True)
    category = serializers.PrimaryKeyRelatedField(many=True, queryset=Category.objects.all())
    product_description_set = ProductDescriptionSerializer(required=False, many=True, write_only=True)
    
    class Meta:
        model = Product
        fields = (
            'id', 'description', 'created_at', 
            'category', 'stock', 'name', 'rate',
            'slug', 'display_image', 'price', 'is_best_seller',
            'discount', 'is_ratable', 'product_description_set', 'first_variant_id'
        )
        extra_kwargs = {
            "display_image" : {"required" : False}
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.context['request'].method == 'GET':                
            data['price'] = price_converter(data['price'] or 0)
        return data


class ProductSerializer(NestedCreateMixin, BaseProductDisplaySerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    items = ProductVariantSerializer(many=True, required=True, source="product_variant_set")

    def validate_items(self, data):
        if len(data) > 3 :
            raise ValidationError("items can only up to 3", code="max_items_length")
        return data

    class Meta(BaseProductDisplaySerializer.Meta):
        fields = BaseProductDisplaySerializer.Meta.fields + ('user', 'items')


class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('is_active', 'is_online', 'category', 'display_image', 'is_ratable')


class ProductDisplaySerializer(BaseProductDisplaySerializer):
    pass


class ProductRetrieveOverViewSerializer(ProductSerializer):
    product_description_set = ProductDescriptionSerializer(required=False, many=True)
    
    class Meta(ProductSerializer.Meta):
        fields = ProductSerializer.Meta.fields + ('user', 'items')


class OverViewProductSerachSerializer(serializers.ModelSerializer):
    items = OverViewSearchProductVariantSerializer(many=True, required=True, source="product_variant_set")
    name = TranslationSerializer(many=True, required=True)
    description = TranslationSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields =  fields = (
            'id', 'description', 'created_at', 'name',
            'slug', 'display_image', 'items'
        )
        
        
