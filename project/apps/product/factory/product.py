import factory
from ..models import Product
from user.models import User
from utils.mixins import FactorySlugMixin
from .description import ProductDescriptionFactory
from .variant import ProductVariantFactory
    
class ProductFactory(FactorySlugMixin):    
    display_image = factory.django.ImageField(color='blue')
    user = factory.Sequence(lambda n : User.objects.order_by('?').first())
    
    class Meta:
        model = Product
    
    @classmethod    
    def build_batch(cls, size, **kwargs):
        product_list : list[Product] = super().build_batch(size, **kwargs)
        for product in product_list:
            product.save()
            
            ProductVariantFactory.build_batch(3, product=product)
            ProductDescriptionFactory.build_batch(3, product=product)
            
            product.name.add(*cls.generate_translations())
            
            product.description.add(*cls.generate_translations())
            
            product.category.add(*cls.get_categories())
            
            product.save()
        return product_list
    