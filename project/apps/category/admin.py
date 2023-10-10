from django.contrib import admin
from .models import Category, Menu, MenuItem
# Register your models here.

admin.site.register([Category, Menu, MenuItem])