from rest_framework import serializers
from user.models import User, OTP

class PromoteUserPermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        extra_kwargs = {
            'email' : {"read_only" : True}
        }
        fields = ('is_staff', 'email', 'id')
        

class ActivateUserSerializer(serializers.Serializer):
    otp = serializers.SlugRelatedField(
        slug_field="otp", queryset=OTP.objects.filter(otp_type=OTP.OTPChoices.ACTIVATE)
    )
    
    class Meta:
        fields = ('otp', )