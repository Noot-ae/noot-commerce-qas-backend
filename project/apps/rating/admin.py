from django.contrib import admin
from .models import ProductRating, VenderRating
# Register your models here.

admin.site.register([ProductRating, VenderRating])