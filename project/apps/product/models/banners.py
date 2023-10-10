from django.db import models
from utils.fields import LimitedImageField

class Carousel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField()
    page = models.ForeignKey('page.Section', models.CASCADE)


class Banner(models.Model):
    carousel = models.ForeignKey(Carousel, models.CASCADE)
    content = models.ManyToManyField('translations.Translation', blank=True, related_name="product_banner_content_set")
    title = models.ManyToManyField('translations.Translation', blank=True, related_name="product_banner_title_set")
    sub_title = models.ManyToManyField('translations.Translation', blank=True, related_name="product_banner_sub_title_set")
    button_text = models.ManyToManyField('translations.Translation', blank=True, related_name="product_button_text_set")
    
    thumbnail = LimitedImageField(blank=True, null=True)
    product_image = LimitedImageField(blank=True, null=True)
    
    redirect_url = models.CharField(blank=True, null=True, max_length=64)
    
    deadline = models.DateTimeField(blank=True, null=True)
    color = models.CharField(blank=True, null=True, max_length=32)
    show_title = models.BooleanField(default=True)    
    