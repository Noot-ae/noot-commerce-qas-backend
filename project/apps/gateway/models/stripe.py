from .base import BaseGateway
from django.db import models

class Stripe(BaseGateway):
    web_hook_secret = models.CharField(max_length=1024)
    publishable_key = models.CharField(max_length=1024)
    secret_key = models.CharField(max_length=1024)
