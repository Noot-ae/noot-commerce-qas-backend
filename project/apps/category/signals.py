from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Category, Menu
from utils.cache import clear_tenant_cache, get_current_schema_name


@receiver([post_save, post_delete], sender=Category)
def category_cache(sender : Category, instance : Category, *args, **kwargs):
    clear_tenant_cache.delay(get_current_schema_name())


@receiver([post_save, post_delete], sender=Menu)
def menu_cache(sender : Menu, instance : Menu, *args, **kwargs):
    clear_tenant_cache.delay(get_current_schema_name())
