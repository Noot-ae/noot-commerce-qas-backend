from ..models import ProductVariant
import factory
from utils.mixins import FactorySlugMixin
import random

MAX_NUMBER = 1000
MIN_NUMBER = 5

get_random_number = lambda *args, **kwargs : random.randrange(MIN_NUMBER, MAX_NUMBER)

class ProductVariantFactory(FactorySlugMixin):
    price = factory.LazyAttribute(get_random_number)
    quantity = factory.LazyAttribute(get_random_number)

    class Meta:
        model = ProductVariant
         
    
    @classmethod    
    def build_batch(cls, size, **kwargs):
        product = kwargs.get('product', cls.get_random_product())
        product_variant_list : list[ProductVariant] = super().build_batch(size, **kwargs)
        for variant in product_variant_list:
            variant.product = product
            variant.save()
        return product_variant_list
    
    