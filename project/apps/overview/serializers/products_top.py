from rest_framework import serializers
from product.models import Product
from translations.serializers import TranslationSerializer


class ProductTopSerializer(serializers.ModelSerializer):
    name = TranslationSerializer(many=True)
    rate = serializers.FloatField(read_only=True)
    price = serializers.FloatField(read_only=True)
    amount_sold = serializers.IntegerField(read_only=True)

    
    class Meta:
        model = Product
        fields = ['id', 'name', 'display_image', 'rate', 'price', 'amount_sold']