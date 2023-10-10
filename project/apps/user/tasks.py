from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task()
def send_otp_mail(to_email: str, message, mail_subject="Welcome to our E-COMMERCE"):
    send_mail(
        subject= mail_subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to_email]
    )