from django.contrib import admin
from .models import Product, ProductVariant, VariantAttribute, Attribute, ProductImage, CartItem, Carousel, Banner, AttributeValue, ProductDescription, WishItem

# Register your models here.

admin.site.register([Product, ProductVariant, VariantAttribute, Attribute,
                     ProductImage, CartItem, Carousel, Banner, AttributeValue, 
                     ProductDescription, WishItem
])
