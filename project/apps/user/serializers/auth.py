from rest_framework import serializers
from .user import UserLoggedInSerializer
from ..tokens import PasswordResetToken, CustomTokenObtainPairSerializer
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from ..models import OTP, User
from django.contrib.auth.models import update_last_login
from django.db import IntegrityError

class JWTLoginSerializer(CustomTokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        update_last_login(None, self.user)
        data['user'] = UserLoggedInSerializer(self.user).data
        return data
    

class SignUpSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only = True, source="password", style={'input_type' : 'password'})
    password2 = serializers.CharField(write_only = True, style={'input_type' : 'password'})

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs['password'] != attrs['password2']:
            raise ValidationError("password do not match each other", code="invalid_passwords")
        attrs.pop('password2')
        validate_password(attrs['password'])
        return attrs

    def create(self, validated_data):
        try:
            return User.objects.create_user(**validated_data, is_active=False)
        except IntegrityError as e:
            raise ValidationError("username already exists", code="unique")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        refresh_token = CustomTokenObtainPairSerializer.get_token(user=instance)
        data["refresh"] = str(refresh_token)
        data["access"] = str(refresh_token.access_token)
        return data

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'password1', 'password2')
        extra_kwargs = {
            'first_name' : {'required' : True},
            'last_name' : {'required' : True},
            'email' : {'required' : True},
        }


class PasswordSendResetSerializer(serializers.ModelSerializer):
    """send reset otp serializer"""
    email = serializers.SlugRelatedField(slug_field="email", queryset=User.objects.all(), source="object", write_only=True)
    otp_type = serializers.HiddenField(default=OTP.OTPChoices.RESET)

    def create(self, validated_data):
        validated_data['object'] = validated_data['object'].email
        return super().create(validated_data)

    class Meta:
        model = OTP
        fields = ('email', 'otp_type')


class PasswordResetVerifySerializer(serializers.ModelSerializer):
    otp = serializers.SlugRelatedField(slug_field="otp", queryset=OTP.objects.filter(otp_type=OTP.OTPChoices.RESET))

    class Meta:
        model = OTP
        fields = ('otp',)

    def create(self, validated_data):
        return validated_data['otp'].user

    def to_representation(self, instance):
        data = {}
        token = PasswordResetToken.get_token(instance)
        data['access'] = str(token.access_token)
        return data


class UpdatePasswordMixin(serializers.Serializer):
    new_password = serializers.CharField(required=True,  style={'input_type' : "password"})
    
    def update(self, instance : User, validated_data):
        instance.set_password(validated_data['new_password'])
        if not instance.is_active:
            instance.is_active = True
        self.instance : User = instance.save()
        return instance
    
    def to_representation(self, instance):
        data = {}
        token = CustomTokenObtainPairSerializer.get_token(instance)
        data['refresh'] = str(token)
        data['access'] = str(token.access_token)
        return data


class PasswordChangeSerializer(UpdatePasswordMixin):
    old_password = serializers.CharField(required=True, style={'input_type' : "password"})

    def validate_old_password(self, value):
        self.instance : User = self.context['request'].user
        if not self.instance.check_password(value):
            raise ValidationError("old passwords doesn't match your password", "invalid_passwords")
        return value


class PasswordResetChangeSerializer(UpdatePasswordMixin):    
    def validate(self, attrs):
        OTP.objects.filter(object=self.instance.email, otp_type=OTP.OTPChoices.RESET).delete()
        return super().validate(attrs)
    
    