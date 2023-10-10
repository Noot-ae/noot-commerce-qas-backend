from django.contrib import admin
from .models import Post, Subscription
# Register your models here.

admin.site.register([Post, Subscription])
