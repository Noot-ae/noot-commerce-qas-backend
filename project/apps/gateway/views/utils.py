from rest_framework.views import APIView
from utils.cache import get_base_currency_factors
from utils.mixins import CacheResponseMixin
from rest_framework.response import Response


class GetCurrencyFactorsView(CacheResponseMixin, APIView):
    cache_timeout = 60 * 60 * 24
    permission_classes = []
    authentication_classes = []
    
    def get(self, request):
        return Response(
            get_base_currency_factors(self.default_currency_code)
        )

    @property
    def default_currency_code(self) -> str:
        return self.request.tenant.currency_code.lower()
    
    def use_cache(self):
        return False