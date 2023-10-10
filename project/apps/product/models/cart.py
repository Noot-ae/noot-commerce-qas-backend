from django.db import models
from django.conf import settings

class CartItem(models.Model):
    user = models.ForeignKey("user.User", models.CASCADE)    
    product = models.ForeignKey('product.ProductVariant', models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def product_names(self):
        return ""