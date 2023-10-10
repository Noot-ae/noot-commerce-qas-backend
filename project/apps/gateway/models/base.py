from django.db import models

# Create your models here.
class BaseGateway(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    success_url = models.URLField()
    cancel_url = models.URLField()
    is_active = models.BooleanField(default=True, unique=True)
    
    PAYMENT_SUCCESS_URL =  lambda self, host : f"{host}/credits/purcashe?message=success"
    PAYMENT_CANCEL_URL =  lambda self, host : f"{host}/credits/purcashe?message=cancel"
    
    class Meta:
        abstract = True