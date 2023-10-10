from rest_framework import serializers
from django.contrib.auth import get_user_model
from vender.models import Vender

User = get_user_model()

class CustomerDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')
        

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'avatar')        


class UserLoggedInSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField(method_name="role_handler")

    def role_handler(self, user):
        if user.is_superuser:
            return "superuser"
        if Vender.objects.filter(user=user).exists():
            return "vender"
        else:
            return "customer"

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'role', 'avatar')
        

class UserListSerializer(UserLoggedInSerializer):
    is_vender = serializers.BooleanField(read_only=True)
    
    class Meta(UserLoggedInSerializer.Meta):
        fields = UserLoggedInSerializer.Meta.fields + ('is_vender', 'is_active', 'is_staff', 'is_blocked')
        
       
class UserDisplaySerializer(serializers.ModelSerializer):
    is_vender = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'role')