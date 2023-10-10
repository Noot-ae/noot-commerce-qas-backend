from ..models import UserPhone, User
from rest_framework.serializers import CurrentUserDefault, HiddenField, ModelSerializer, PrimaryKeyRelatedField


class GuestUserPhoneSerializer(ModelSerializer):
    class Meta:
        model = UserPhone
        fields = ['id', 'phone']
        
        
class UserPhoneSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = UserPhone
        fields = '__all__'


class PhoneDashboardSerializer(UserPhoneSerializer):
    user = PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

