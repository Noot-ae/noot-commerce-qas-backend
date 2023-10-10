from django.db import models
from utils.fields import LimitedImageField

def product_image_handler(instance, filename):
    return f"products/{instance.product_variant.product_id}/variants-{instance.product_variant_id}/images/{filename}"


class ProductImage(models.Model):
    product_variant = models.ForeignKey('product.ProductVariant', models.CASCADE, blank=True, related_name="variant_image_set")
    image = LimitedImageField(upload_to=product_image_handler, blank=False, null=False)


