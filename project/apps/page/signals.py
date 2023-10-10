from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Section
from utils.cache import clear_tenant_cache, get_current_schema_name


@receiver(post_save, sender=Section)
def page_cache(sender : Section, instance : Section, *args, **kwargs):
        clear_tenant_cache.delay(get_current_schema_name())
