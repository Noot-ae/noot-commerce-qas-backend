from ..models import ProductImage, ProductVariant
from rest_framework import serializers
from django.db.models import Count
from rest_framework.exceptions import ValidationError

class ProductImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductImageCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.FileField(), required=True, write_only=True, max_length=3)
    product_variant = serializers.PrimaryKeyRelatedField(queryset=ProductVariant.objects.annotate(total_images=Count("variant_image_set")).all())

    def create(self, validated_data):
        images =  ProductImage.objects.bulk_create(
            [ProductImage(image=image, product_variant=validated_data['product_variant']) for image in validated_data['images']]
        )
        return images[0]
    
    def validate(self, attrs):
        attrs = super().validate(attrs)
        images_count = len(attrs['images'])
        max_images_to_upload = attrs['product_variant'].total_images or 3
        if images_count > max_images_to_upload:
            raise ValidationError(f'max images are: {attrs["product_variant"].total_images - images_count}', code="max_images_limit")
        return attrs
        
    class Meta:
        model = ProductImage
        fields = ('images', 'product_variant')
    