from django.db import models

class Paymob(models.Model):
    is_active = models.BooleanField(default=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    iframe_id = models.PositiveIntegerField()
    integration_id = models.PositiveIntegerField()
    api_key = models.TextField(max_length=512)
    hmac_secret = models.TextField(max_length=512)
    currency = models.CharField(max_length=6, default="EGP")

    def __str__(self) -> str:
        return f"iframe: {self.iframe_id} - integration_id: {self.integration_id}"