from rest_framework import serializers
from .models import Vender
from drf_writable_nested.serializers import WritableNestedModelSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()

class VenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vender
        fields = '__all__'
        extra_kwargs = {
            'user' : {"required" : False}
        }


class VenderRegisterSerializer(WritableNestedModelSerializer):
    vender = VenderSerializer()

    def validate_password(self, value):
        return make_password(value)
    
    def is_superuser(self):
        user = self.context['request'].user 
        return all([user, user.is_authenticated, user.is_superuser])
    
    def create(self, validated_data):
        validated_data['is_active'] = self.is_superuser()
        return super().create(validated_data)
    
    
    class Meta:
        model = User
        fields = ('id', 'vender', 'username', 'email', 'password', 'first_name', 'last_name',)
        
        