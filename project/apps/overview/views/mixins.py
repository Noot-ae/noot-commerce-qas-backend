from rest_framework.permissions import IsAdminUser, DjangoModelPermissions
from rest_framework.settings import api_settings


class BaseViewMixin:
    permissions_classes = (IsAdminUser | DjangoModelPermissions,)
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES
