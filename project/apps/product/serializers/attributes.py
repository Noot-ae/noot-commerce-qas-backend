from rest_framework import serializers
from ..models import VariantAttribute, ProductVariant, AttributeValue


class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = '__all__'
        extra_kwargs = {
            "attribute" : {"required" : False}
        }

class VariantAttributeSerializer(serializers.ModelSerializer):
    attribute_name = serializers.CharField(read_only=True, source="attribute.name")
    attribute_value = AttributeValueSerializer(read_only=True, source="value")

    class Meta:
        model = VariantAttribute
        fields = ('id', 'value', 'attribute', 'attribute_name', 'product_variant_id', 'attribute_value')
        extra_kwargs = {"product_variant" : {"required" : False, "write_only" : True}}


class VriantUpdateAttributeSerializer(serializers.ModelSerializer):
    variant_attribute_set = serializers.ListField(child=VariantAttributeSerializer(), required=False)
    product_variant = serializers.PrimaryKeyRelatedField(queryset=ProductVariant.objects.all())

    def create(self, validated_data):
        variant_attribute_data = validated_data.get('variant_attribute_set', [])
        VariantAttribute.objects.bulk_create(
            [VariantAttribute(**d, product_variant=validated_data['product_variant']) for d in variant_attribute_data]
        )
        return VariantAttribute.objects.none()

        
    class Meta:
        model = VariantAttribute
        fields = ('variant_attribute_set', 'product_variant')