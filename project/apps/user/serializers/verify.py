from rest_framework import serializers
from ..models import User, OTP
from rest_framework.exceptions import ValidationError

class DummyOtp:
    object = None


class CurrentUserEmailDefault(serializers.CurrentUserDefault):
    def __call__(self, serializer_field):
        return super().__call__(serializer_field).email


class EmailChangeSerializer(serializers.ModelSerializer):
    otp = serializers.SlugRelatedField(queryset=OTP.objects.filter(otp_type=OTP.OTPChoices.VERIFY), slug_field="otp", write_only=True, required=True)
    old_otp = serializers.SlugRelatedField(queryset=OTP.objects.filter(otp_type=OTP.OTPChoices.VERIFY), slug_field="otp", write_only=True, required=True)
    email = serializers.EmailField()

    def validate(self, attrs):
        old_otp_is_valid = (attrs.get('old_otp', DummyOtp).object == self.context['request'].user.email)
        new_otp_is_valid = (attrs.get('otp', DummyOtp).object == attrs.get('email'))

        if old_otp_is_valid and new_otp_is_valid:
            return super().validate(attrs)
        raise ValidationError("invalid_otp", code="invalid_otp")

    def update(self, instance, validated_data):
        validated_data.pop("otp")
        return super().update(instance, validated_data)

    class Meta:
        model = User
        fields = ('otp', 'email', 'old_otp')


class SendEmailVerifyOTPSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="object")    
    otp_type = serializers.HiddenField(default=OTP.OTPChoices.VERIFY)

    class Meta:
        model = OTP
        fields = ('email', 'otp_type')

    def validate_email(self, value):
        exists = User.objects.filter(email=value).exists()
        if not exists:
            raise ValidationError("email does not exist", code="not_found")
        return value

    def create(self, validated_data):
        return super().create(validated_data)


class SendUserEmailVerifyOTPSerializer(SendEmailVerifyOTPSerializer):
    email = serializers.EmailField(default=CurrentUserEmailDefault(), source="object")


class VerifyOtpUsernameSerializer(serializers.Serializer):
    otp = serializers.SlugRelatedField(slug_field="otp", queryset=OTP.objects.filter(otp_type=OTP.OTPChoices.VERIFY))

    class Meta:
        fields = ('otp',)

    def create(self, validated_data):
        return validated_data['otp'].user

    def to_representation(self, instance : User):
        data = {}
        data['username'] = str(instance.username)
        return data