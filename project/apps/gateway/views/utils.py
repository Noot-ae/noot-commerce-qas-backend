from rest_framework.views import APIView
from utils.cache import get_base_currency_factors
from utils.mixins import CacheResponseMixin
from rest_framework.response import Response
from user.models import Region
import logging


class GetCurrencyFactorsView(CacheResponseMixin, APIView):
    cache_timeout = 60 * 60 * 24
    permission_classes = []
    authentication_classes = []
    
    def get(self, request):
        return Response(
            self.get_factors(
                get_base_currency_factors(self.default_currency_code)
            )
        )

    def get_active_currency_codes(self) -> list[str]:
        active_currencies = list(
            Region.objects.all().distinct('currency_code').values_list('currency_code', flat=True)
        )
        return active_currencies
        
    def get_factors(self, _factors : dict) -> list[dict]:
        factors = []
        for code in self.get_active_currency_codes():
            try:
                factors.append(
                    {
                        "code" : code,
                        "factor" : _factors.get(self.default_currency_code, {})[code.lower()]
                    }           
                )
            except KeyError as e:
                logging.warning(f"invalid code {code}")
        return factors
    
    @property
    def default_currency_code(self) -> str:
        return self.request.tenant.currency_code.lower()
    
    def use_cache(self):
        return False