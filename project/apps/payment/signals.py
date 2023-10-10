from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Refund, Payment


@receiver(post_save, sender=Payment)
def after_payment(sender: Payment, instance : Payment, **kwargs):
    if not kwargs.get('created', False): return
    instance.order.activate_order()


@receiver(post_save, sender=Refund)
def after_refund(sender: Refund, instance : Refund, **kwargs):
    if not kwargs.get('created', False): return
    instance.do_refund()    
        
        
