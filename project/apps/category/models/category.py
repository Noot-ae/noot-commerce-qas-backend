from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.core.validators import FileExtensionValidator
from utils.fields import LimitedImageField

# Create your models here.
def category_img_handler(instance, filename):
    return f"categories/{instance.id} - {instance.slug}/{filename}"


class Category(MPTTModel):
    base_category = TreeForeignKey('self', models.CASCADE, blank=True, null=True, related_name="sub_categories")
    names = models.ManyToManyField('translations.Translation', related_name="category_names_translations")
    descriptions = models.ManyToManyField('translations.Translation', related_name="category_descriptions_translations")
    slug = models.SlugField(unique=True)
    thumbnail = LimitedImageField(upload_to=category_img_handler, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    icon = models.FileField(blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['svg'])])
    
    class MPTTMeta:
        parent_attr = 'base_category'    

