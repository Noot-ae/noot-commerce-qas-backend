from django.db import models
from django.core.validators import MinValueValidator
from orders.models import OrderProduct
import random
import string
from utils.fields import LimitedImageField
from utils.price_converter import price_converter

# Create your models here.
class Product(models.Model):
    category = models.ManyToManyField('category.Category', blank=True)
    user = models.ForeignKey("user.User", models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    is_ratable = models.BooleanField(default=True)
    display_image = LimitedImageField(null=True, blank=True)
    #set to false to disable purcashe, add to card
    is_active = models.BooleanField(default=True)

    #set to false to disable showing it in the search
    is_online = models.BooleanField(default=True)

    slug = models.SlugField(unique=True, null=True, blank=True)

    #used to promote these items in recommendation
    similar_products = models.ManyToManyField('self', blank=True)

    description = models.ManyToManyField('translations.Translation', related_name='product_description_translations_set', blank=True)
    name = models.ManyToManyField('translations.Translation', related_name="product_name_translations_set", blank=True)

    def is_owner(self, user):
        return user == self.user
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.set_slug()
        return super().save(*args, **kwargs)
    
    def set_slug(self):
        self.slug = "".join(random.choices(string.ascii_lowercase))
        if self.__class__.objects.filter(slug=self.slug).exists():
            self.set_slug()
    
    @property
    def total_quantity(self):
        if hasattr(self, 'stock'):
            return self.stock
        
        _ = self.productvarient_set.aggregate(stock=models.Sum('quantity'))
        self.stock = _['stock']
        return self.stock
        
    @property
    def get_productvariant_set(self):
        if getattr(self, '_product_variant_set', False):
            return self._product_variant_set
        return self.product_variant_set

    @property
    def in_stock(self):
        return self.total_quantity > 0


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, models.CASCADE, blank=True, related_name="product_variant_set")
    discount = models.FloatField(default=0, validators=[MinValueValidator(0)])
    price = models.FloatField()
    quantity = models.PositiveIntegerField()
    slug = models.SlugField(blank=True, null=True)

    def change_quantity(self, value):
        self.quantity = models.F("quantity") + value
        self.save(update_fields=['quantity'])
        self.refresh_from_db(fields=['quantity'])        

    def reduce_quantity(self, value):
        return self.change_quantity(-abs(int(value)))
    
    def images_set(self):
        if getattr(self, '_images_set', []):
            return self._images_set
        return self.variant_image_set.all()
    
    def __str__(self) -> str:
        return f"{self.id} - {self.slug}"
    
    @property
    def has_orders(self):
        if hasattr(self, '_has_orders'):
            return self._has_orders
        return OrderProduct.objects.filter(product_variant=self).exists()
    
    def get_exchanged_price(self):
        return price_converter(self.price)


class ProductDescription(models.Model):
    product = models.ForeignKey(Product, models.CASCADE, blank=True, related_name="product_description_set")
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.ManyToManyField('translations.Translation', related_name='product_section_description_translations_set', blank=True)
    name = models.ManyToManyField('translations.Translation', related_name="product_section_name_translations_set", blank=True)
    is_active = models.BooleanField(default=True)

