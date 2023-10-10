from django.contrib import admin
from .models import Stripe, Paymob, Currency
# Register your models here.

admin.site.register([Stripe, Paymob, Currency])