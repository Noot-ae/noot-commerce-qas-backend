from django.db import models


class VariantAttribute(models.Model):
    attribute = models.ForeignKey('product.Attribute', models.SET_NULL, blank=True, null=True, related_name="variant_attribute_set")
    value = models.ForeignKey('product.AttributeValue', models.SET_NULL, blank=True, null=True, related_name="variant_attribute_set")
    product_variant = models.ForeignKey('product.ProductVariant', models.CASCADE, related_name="variant_attribute_set")
    

class Attribute(models.Model):
    name = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class AttributeValue(models.Model):
    attribute = models.ForeignKey('product.Attribute', models.SET_NULL, blank=True, null=True, related_name="attribute_value_set")
    value = models.CharField(max_length=64)
    extra_data = models.JSONField(blank=True, null=True)
