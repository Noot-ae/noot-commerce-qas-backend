from rest_framework_simplejwt.authentication import JWTAuthentication, api_settings, AuthenticationFailed, InvalidToken
from django.db import connection
from vender.models import Vender
from django.db.models import Exists, F, Prefetch
from .models import ShipmentProfile, User
from django.utils.translation import gettext_lazy as _

class TenantAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        try:                
            assert connection.schema_name == validated_token['schema_name'], "token not valid for schema"
        except Exception as e:
            raise AuthenticationFailed(e, code="invalid_schema")
        
    
        try:
            user_id = int(
                validated_token[api_settings.USER_ID_CLAIM]
            )
        except (KeyError, ValueError):
            raise InvalidToken(_("Token contained no recognizable user identification"))
        try:
            user : User = self.get_user_query().annotate(is_vender = Exists(Vender.objects.filter(user__id = F('pk')))).get(**{api_settings.USER_ID_FIELD: user_id})
            assert not user.is_blocked
        except self.user_model.DoesNotExist:
            raise AuthenticationFailed(_("User not found"), code="user_not_found")
        except AssertionError as e:
            raise AuthenticationFailed("user_is_blocked", code="user_is_blocked")
        if not user.is_active:
            raise AuthenticationFailed(_("User is inactive"), code="user_inactive")
        return user
    
    def get_user_query(self):
        return self.user_model.objects.all()
    
    
class ProfileAuth(TenantAuthentication):
    def get_user_query(self):
        qs = super().get_user_query()
        qs = qs.prefetch_related(Prefetch(lookup="shipmentprofile_set", queryset=ShipmentProfile.objects.select_related('phone_number')))
        return qs
    