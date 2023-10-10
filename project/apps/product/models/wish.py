from django.db import models


class WishItem(models.Model):
    user = models.ForeignKey("user.User", models.CASCADE, related_name="wisth_item_set")
    created_at = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey('product.ProductVariant', models.CASCADE, related_name="as_wish_set")
