from django.db import models
import string
import random
from .user import User
from django.shortcuts import get_object_or_404

# Create your models here.
class OTP(models.Model):
    class OTPChoices(models.TextChoices):
        VERIFY = "VERIFY"
        RESET = "RESET"
        ACTIVATE = "ACTIVATE"
    
    class VerifyChoices(models.TextChoices):
        EMAIL = "EMAIL"
        PHONE = "PHONE"
    
    otp_type = models.CharField(max_length=16, choices=OTPChoices.choices, default=OTPChoices.ACTIVATE)
    verify_type = models.CharField(choices=VerifyChoices.choices, default=VerifyChoices.EMAIL, max_length=20)

    object = models.CharField(max_length=64)
    otp = models.CharField(max_length=12, blank=True, db_index=True)


    def save(self, *args, **kwargs):
        if (not self.pk) and (not self.otp):
            self.set_otp()
        return super().save(*args, **kwargs)
    
    def set_otp(self):
        letters = string.ascii_lowercase
        self.otp = ''.join(random.choice(letters) for i in range(6))

    def __str__(self) -> str:
        return f"{self.otp} - {self.object}"
    
    @property
    def user(self):
        if self.verify_type == self.VerifyChoices.EMAIL:
            return get_object_or_404(User, email=self.object)
        