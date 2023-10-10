from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import OTP, User
from vender.models import Vender
from django.db import connection
from .tasks import send_otp_mail


@receiver(post_save, sender=OTP)
def after_otp(sender: OTP, instance : OTP, **kwargs):
    if not kwargs.get('created', False): return
    message = f"Hello, this is your otp {instance.otp}, please don't share it with others."
    send_otp_mail.delay(instance.object, message,mail_subject="Password Reset")


@receiver(post_save, sender=User)
def after_user(sender: User, instance : User, **kwargs):
    if not kwargs.get('created', False): return
    if connection.schema_name == "public" : return
    if instance.is_superuser:
        Vender.objects.create(user=instance)


@receiver(post_save, sender=User)
def send_user_signup_otp(sender : User, instance: User, *args, **kwargs):
    if not kwargs.get('created', False): return
    if instance.is_active: return
    OTP.objects.create(object=instance.email)

