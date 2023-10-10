from django.db import models
from django_tenants.models import TenantMixin, DomainMixin
import random
from string import ascii_lowercase
from .utils import ThemeGenerator


class Client(TenantMixin):
    created_on = models.DateField(auto_now_add=True)
    username = models.CharField(max_length=250)
    
    currency_name = models.CharField(max_length=128)
    currency_code = models.CharField(max_length=16)
    currency_symbol = models.CharField(max_length=16, blank=True, null=True)
    
    allow_purchase = models.BooleanField(default=True)
    is_enabled = models.BooleanField(default=True)

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True
    auto_drop_schema = True

    def save(self, verbosity=1, *args, **kwargs):
        if not self.schema_name:
            self.set_schema_name()
        return super().save(verbosity, *args, **kwargs)

    def set_schema_name(self):
        random_name = ''.join(random.choices(ascii_lowercase, k=24))
        self.schema_name = f"schema_{random_name}"

    @staticmethod
    def generate_theme(theme_name):
        return ThemeGenerator(theme_name).generate()


class Domain(DomainMixin):
    pass