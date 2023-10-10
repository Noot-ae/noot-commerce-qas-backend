from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from vender.models import Vender
from django.db.models import Exists, OuterRef
from rest_framework.exceptions import ValidationError

UserModel = get_user_model()

class CustomBackend(ModelBackend):
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        if username is None or password is None:
            return
        try:
            user = UserModel._default_manager.annotate(
                    is_vender = Exists(Vender.objects.filter(user=OuterRef('pk')))
                ).get(**{UserModel.USERNAME_FIELD : username})
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
            
            
    def user_can_authenticate(self, user):
        is_vender = getattr(user, 'is_vender', None)
        is_active = getattr(user, "is_active", None)
        
        if is_vender and not is_active:
            raise ValidationError("Admin has not activated your vender account yet.", code="inactive_account")
        
        return is_active or is_active is None