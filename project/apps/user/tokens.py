from rest_framework_simplejwt.authentication import JWTAuthentication, AuthenticationFailed, InvalidToken, api_settings
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db import connection

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['schema_name'] = connection.schema_name

        return token


class PasswordResetAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        if not validated_token.get('type', False) == "reset_password":
            raise AuthenticationFailed(('Bad Token'), code='user_inactive')
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError:
            raise InvalidToken(("Token contained no recognizable user identification"))

        try:
            user = self.user_model.objects.get(**{api_settings.USER_ID_FIELD: user_id})
        except self.user_model.DoesNotExist:
            raise AuthenticationFailed(("User not found"), code="user_not_found")
        return user


class PasswordResetToken(CustomTokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['type'] = "reset_password"
        return token