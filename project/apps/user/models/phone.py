from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class UserPhone(models.Model):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, blank=True, null=True, related_name="user_phone_set")
    created_at = models.DateTimeField(auto_now_add=True)
    phone = PhoneNumberField(unique=True)
    