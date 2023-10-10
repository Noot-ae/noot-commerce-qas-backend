from django.db import models
from user.models import User
from utils.fields import LimitedImageField


# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User, models.CASCADE, related_name="user_posts")
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.ManyToManyField('translations.Translation', related_name="post_title_translations_set", blank=True)
    body = models.ManyToManyField('translations.Translation', related_name="post_body_translations_set", blank=True)
    thumbnail = LimitedImageField(blank=True, null=True)
    slug = models.SlugField(unique=True, null=True)
    

class Subscription(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
