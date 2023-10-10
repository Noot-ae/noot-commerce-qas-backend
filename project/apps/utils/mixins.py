import factory
from django.views.decorators.cache import cache_page
from django.conf import settings
from translations.factory import TranslationFactory
from category.models import Category
import random
from string import ascii_letters
from product.models import Product

class CacheResponseMixin:
    
    cache_timeout = 60 * 5

    def get_cache_timeout(self):
        return self.cache_timeout

    def dispatch(self, *args, **kwargs):
        if not self.use_cache():
            return super().dispatch(*args, **kwargs)
        return cache_page(self.get_cache_timeout())(super().dispatch)(*args, **kwargs)
    
    def use_cache(self):
        return settings.USE_CACHE


class FactoryMixin(factory.django.DjangoModelFactory):
    @staticmethod
    def generate_translations(length=2):
        translation_list =  TranslationFactory.build_batch(length)
        [translation.save() for translation in translation_list]
        return translation_list
        
    @staticmethod
    def get_categories(limit=2):
        return Category.objects.all().order_by('?')[:limit]
    
    @classmethod
    def get_random_product(cls):
        return Product.objects.all().order_by('?').first()   
    
    
class FactorySlugMixin(FactoryMixin):
    slug = factory.Sequence(lambda x : f"sluggy-{x}-{''.join(random.choices(ascii_letters, k=5))}")

