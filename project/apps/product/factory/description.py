from ..models import ProductDescription
from utils.mixins import FactoryMixin

    
class ProductDescriptionFactory(FactoryMixin):    
    class Meta:
        model = ProductDescription
    
    @classmethod    
    def build_batch(cls, size, **kwargs):
        product = kwargs.get('product', cls.get_random_product())
        description_list : list[ProductDescription] = super().build_batch(size, **kwargs)
        for description in description_list:
            description.product = product
            description.save()
            description.name.add(*cls.generate_translations())            
            description.description.add(*cls.generate_translations())
            description.save()
            
        return description_list