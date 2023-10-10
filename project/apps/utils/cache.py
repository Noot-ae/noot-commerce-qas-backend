from django.core.cache import cache
from django.db.models import Count
from django.conf import settings
import requests
from django.db import connection
from django.core.exceptions import ValidationError
from gateway.models.currency import Currency, FakeCurrency
from gateway.serializers import CurrencySerializer
from celery import shared_task
import redis


def get_current_schema_name():
    return connection.schema_name

class BaseCached:
    key : str = None
    cache_timeout=24*60*60
    
    
    def get_key_suffix(self):
        if self.key is None:
            raise AttributeError("key attribute must be implemented")
    
    def wrapper(self):
        raise NotImplementedError

    @property
    def cache_key(self):
        return f"{get_current_schema_name()}__{self.get_key_suffix()}"
    
    def __repr__(self) -> str:
        cached_json = cache.get(self.cache_key)
        if cached_json is not None:
            return cached_json
        return self.get_data()

    def get_data(self):
        data = self.wrapper()
        if data:
            self.set_cache_object(data)
        return data
    
    def set_cache_object(self, data):
        cache.set(self.cache_key, data, self.cache_timeout)
        



def set_cache_object(key, data, cache_timeout=24*60*60):
    cache.set(key, data, cache_timeout)

def get_cached_or_retrieve_json(key_suffix, retrieve_function, cache_timeout=None, schema_name=None, *args, **kwargs):
    
    cached_json = cache.get(key_suffix)
    if cached_json is not None:
        return cached_json

    data = retrieve_function(key_suffix, *args, **kwargs)
    if data:
        set_cache_object(key_suffix, data, cache_timeout)

    return data


def call_currency_factor_api(currency: str):
    url = f"https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/{currency.lower()}.json"
    response = requests.get(url)
    try:
        return response.json()
    except Exception as e:
        raise ValidationError(f"there might be a problem with your currency code, original exception: {e}", code="invalid_currency_code")


def call_db_currency(*args, **kwargs):
    return Currency.objects.values("currency_code", "currency_name", "currency_symbol", "created_at", "is_active")


def get_base_currency_factors(currency):
    return get_cached_or_retrieve_json(currency, call_currency_factor_api)


def set_active_currency(*args, **kwargs):
    try:            
        currency = Currency.objects.get(is_active=True)
        data = CurrencySerializer(instance=currency).data
        call_currency_factor_api(currency.currency_code)
        return data
    except Currency.DoesNotExist:
        return FakeCurrency.serialize()
    
def get_active_currency():
    return get_cached_or_retrieve_json(f"{get_current_schema_name()}_active_currency", set_active_currency)


def get_best_seller_sold_amount():
    from product.models import Product
    def wrapper(*args, **kwargs):        
        try:
            return Product.objects.annotate(
                amount_sold = Count('product_variant_set__as_order_item_set__quantity')
            ).order_by('-amount_sold')[:3].only('id').first().amount_sold or 0
        except AttributeError:
            return 0 
    return get_cached_or_retrieve_json(f"{get_current_schema_name()}_top_third_product_seller", wrapper)


class CacheUtils:
    def __init__(self):
        self.connection = redis.Redis.from_url(settings.REDIS_URL)

    def delete_key(self, key):
        self.connection.delete(key)

    def delete_tenant_caches(self, db_schema):
        key = f"{db_schema}::*"
        keys = self.connection.keys(key)
        print([key for key in keys])
        [self.delete_key(key) for key in keys]


@shared_task()
def clear_tenant_cache(db_schema : str = None):
    if not db_schema:
        db_schema = get_current_schema_name()
    _cache = CacheUtils()
    _cache.delete_tenant_caches(db_schema)
