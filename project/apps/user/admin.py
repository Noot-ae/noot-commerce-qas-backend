from django.contrib import admin
from .models import OTP, UserPhone, User, ShipmentProfile, Region, Contact
from django.contrib.auth.models import Permission

# Register your models here. 
admin.site.register([OTP, Permission, UserPhone, ShipmentProfile, User, Region, Contact])
