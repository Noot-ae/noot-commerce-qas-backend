from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator

# Create your models here.
class BaseRating(models.Model):
    user = models.ForeignKey("user.User", models.CASCADE)
    rate = models.PositiveIntegerField(validators=[
            MaxValueValidator(5),
        ])
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        abstract = True


class ProductRating(BaseRating):
    product = models.ForeignKey('product.Product', models.CASCADE)
    likes = models.ManyToManyField("user.User", related_name="user_product_rating_like_set", blank=True)

    class Meta:
        unique_together = ('user', 'product')

class VenderRating(BaseRating):
    vender = models.ForeignKey('vender.Vender', models.CASCADE)
    likes = models.ManyToManyField("user.User", related_name="user_vender_rating_like_set", blank=True)

    class Meta:
        unique_together = ('user', 'vender')


class ProductReply(models.Model):
    user = models.ForeignKey("user.User", models.CASCADE, related_name="product_comment_reply_set")
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=512)
    likes = models.ManyToManyField("user.User", blank=True)
    parent_comment = models.ForeignKey(ProductRating, models.CASCADE, related_name="reply_set")
    parent_reply = models.ForeignKey('self', models.CASCADE, blank=True, null=True)
