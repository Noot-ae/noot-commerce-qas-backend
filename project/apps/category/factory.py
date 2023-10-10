from category.models import Category
from utils.mixins import FactorySlugMixin

class CategoryFactory(FactorySlugMixin):
    
    class Meta:
        model = Category
        
    @classmethod    
    def build_batch(cls, size, **kwargs):
        product_list : list[Category] = super().build_batch(size, **kwargs)
        for product in product_list:
            product.save()
            product.names.add(*cls.generate_translations())
            product.descriptions.add(*cls.generate_translations())
            product.save()       
        return product_list