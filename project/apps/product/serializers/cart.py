from ..models import CartItem
from rest_framework import serializers
from translations.serializers import TranslationSerializer
from .variant import CartVariantSerializer

class CartItemSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    product_names = TranslationSerializer(many=True, read_only=True, source="product.product.name")
    
    
    class Meta:
        model = CartItem
        fields = ('id', 'product', 'created_at', 'product_names', 'user')
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['product'] = CartVariantSerializer(instance.product).data
        return data