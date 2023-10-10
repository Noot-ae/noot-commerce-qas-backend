from rest_framework.authentication import BaseAuthentication

class TenantCreateAuth(BaseAuthentication):

    def authenticate(self, request):
        pass