from utils.cache import set_active_currency
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from .models import Currency


@receiver([post_delete, post_save], sender=Currency)
def currency_signal(*args, **kwargs):
    set_active_currency()