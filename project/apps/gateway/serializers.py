from rest_framework import serializers
from .models import Stripe, Paymob, Currency

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'


class StripeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Stripe
        fields = '__all__'


class PaymobSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Paymob
        fields = '__all__'
