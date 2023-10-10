from django.db import models
from django.db import connection

class Currency(models.Model):
    currency_name = models.CharField(max_length=16)
    currency_code = models.CharField(max_length=16)
    currency_symbol = models.CharField(max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, unique=True)
    
    
class FakeCurrency:
    
    attrs = ["currency_name", "currency_code", "currency_symbol"]
    
    def __init__(self, tenant = None) -> None:
        if not tenant:
            tenant = connection.tenant
            
        for attr in self.attrs:
            setattr(
                self, attr,
                getattr(tenant, attr)
            )
            
    @classmethod
    def serialize(cls):
        instance = cls()
        return {
            key : getattr(instance, key, None) for key in cls.attrs
        }