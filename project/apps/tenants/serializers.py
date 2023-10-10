from rest_framework import serializers
from user.tokens import CustomTokenObtainPairSerializer
from user.serializers import SignUpSerializer
from .models import Client, Domain
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from user.models import User, Region
from translations.models import Translation
from django.db import IntegrityError
from utils.cache import get_active_currency
from utils.price_converter import get_current_tenant_currency_code
from user.models import Region


class ClientUserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only = True, source="password", style={'input_type' : 'password'})
    password2 = serializers.CharField(write_only = True, style={'input_type' : 'password'})

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs['password'] != attrs['password2']:
            raise ValidationError("password do not match each other", code="invalid_passwords")
        attrs.pop('password2')
        validate_password(attrs['password'])
        return attrs

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
        extra_kwargs = {
            'schema_name' : {"read_only" : True}
        }


class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = '__all__'
        extra_kwargs = {
            'tenant' : {"required" : False}
        }


class TenantSerializer(serializers.ModelSerializer):
    THEME_CHOICES =( 
        ("commerce", "commerce"),
        ("legacy", "legacy"),
        ("cosmetics", "cosmetics"),
        ("market", "market"),
        ("oasis", "oasis"),
    )
    
    default_country_name = serializers.CharField(write_only=True)
    domain = DomainSerializer(required=True)
    user = ClientUserSerializer(required=True)
    theme_name = serializers.ChoiceField(write_only=True, choices=THEME_CHOICES)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        attrs['username'] = attrs['user']['username']
        return attrs

    def create(self, validated_data : dict):
        user_data = validated_data.pop('user', {})
        domain_data = validated_data.pop('domain')
        theme_name = validated_data.pop('theme_name')
        default_country_name = validated_data.pop('default_country_name')
        
        tenant : Client = super().create(validated_data)
        tenant.activate()
        
        self.generate_default_country(default_country_name)
        user_data = self.create_user(user_data)
        domain_data['tenant'] = tenant
        
        try:
            domain = self.create_domain(domain_data)
        except IntegrityError as e:
            raise ValidationError(f"{e}", code="invalid_domain_data")
        
        tenant.user = user_data
        tenant.domain = domain
        tenant.generate_theme(theme_name)
        return tenant
    
    def create_user(self, data):
        self.user_instance = User.objects.create_superuser(data.pop('username'), **data)
        user_data = SignUpSerializer(instance=self.user_instance).data
        return user_data
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['access_token'] = str(CustomTokenObtainPairSerializer.get_token(self.user_instance).access_token)
        return data

    def create_domain(self, data):
        domain = Domain.objects.create(**data)
        return domain        

    def generate_default_country(self, name):
        code = get_current_tenant_currency_code()
        
        region = Region.objects.create(
            minimum_order_price=0,
            minimum_order_free_ship_price=0,
            fixed_shipment_price=0,
            currency_code=code
        )
        
        region.names.add(
            Translation.objects.create(
                text = name
            )
        )
        region.save()
  

    class Meta:
        model = Client
        fields = (
            'id', 'schema_name', 'username', 'domain', 'user', 'currency_name', 
            'currency_code', 'currency_symbol', 'allow_purchase', 
            'theme_name', 'default_country_name'
        )
        extra_kwargs = {
            'schema_name' : {"read_only" : True}
        }


class CurrencyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('currency_name', 'currency_code', 'currency_symbol', 'allow_purchase')
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['active_currency'] = get_active_currency()
        return data


class TenantUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('currency_name', 'currency_code', 'currency_symbol', 'is_enabled', 'allow_purchase')
        

class TenantOwnerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('currency_name', 'currency_code', 'currency_symbol', 'allow_purchase')
        

