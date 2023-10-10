from rest_framework import serializers
from ..models import OrderProduct
from product.models import ProductVariant
from product.serializers import OrderProductVariantSerializer

class OrderProductListSerializer(serializers.ModelSerializer):
    amount_cents = serializers.FloatField(source="price")
    name = serializers.SerializerMethodField()
    
    def get_name(self, instance : OrderProduct):
        return f"variant with id {instance.product_variant_id}"

    class Meta:
        model = OrderProduct
        fields = ['amount_cents', 'quantity', 'name']

class OrderProductSerializer(serializers.ModelSerializer):
    # product_variant = serializers.PrimaryKeyRelatedField(
    #     queryset=ProductVariant.objects.all().select_for_update('self').select_related('product').prefetch_related('product__name')
    # )
    
    class Meta:
        model = OrderProduct
        fields = '__all__'
        extra_kwargs = {
            'order' : {'required' : False},
            'price' : {'read_only' : True},
            'order_status' : {'required' : False}
        }

    def to_representation(self, instance : OrderProduct):
        data = super().to_representation(instance)
        if self.context['request'].method == 'GET':                
            instance.product_variant._has_orders = True
            data['product_variant'] = OrderProductVariantSerializer(instance=instance.product_variant).data
        return data