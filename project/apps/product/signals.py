from django.db.models.signals import pre_delete, post_save, post_delete
from django.dispatch import receiver
from .models import ProductImage, Product
from utils.cache import clear_tenant_cache, get_current_schema_name


@receiver([post_save, post_delete], sender=Product)
def delete_product_cache(sender, instance, *args, **kwargs):
    clear_tenant_cache.delay(get_current_schema_name())


@receiver(pre_delete, sender=ProductImage)
def delete(sender, instance : ProductImage, *args, **kwargs):
    instance.image.delete()
    
    
