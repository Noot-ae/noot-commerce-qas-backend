from rest_framework import serializers
from utils.serializer_fields import StringCurrentUserRelatedField
from ..models import UserPhone, ShipmentProfile, User
from drf_writable_nested.mixins import NestedCreateMixin
from .phone import PhoneDashboardSerializer, GuestUserPhoneSerializer
from drf_writable_nested import WritableNestedModelSerializer


class GuestShipmentSerializer(WritableNestedModelSerializer):
    phone_number = GuestUserPhoneSerializer()
    class Meta:
        model = ShipmentProfile
        exclude = ['user']
        
        
class ShipmentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    phone_number = StringCurrentUserRelatedField(queryset=UserPhone.objects.all(), slug_field="phone")
    
    class Meta:
        model = ShipmentProfile
        fields = '__all__'
        extra_kwargs = {
            "country" : {"required" : True}
        }


class OverViewShipmentSerializer(NestedCreateMixin, serializers.ModelSerializer):
    phone_number = PhoneDashboardSerializer()
    
    class Meta(ShipmentSerializer.Meta):
        pass


class UserProfileSerializer(serializers.ModelSerializer):
    profiles = ShipmentSerializer(source="shipmentprofile_set", many=True)
    
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username', 'profiles', 'avatar')
        
        

class DashboardShipmentSerializer(ShipmentSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    phone_number = serializers.PrimaryKeyRelatedField(queryset=UserPhone.objects.all())
    
    