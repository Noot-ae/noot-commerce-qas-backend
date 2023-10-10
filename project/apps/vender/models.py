from django.db import models
from django.conf import settings

# Create your models here.
class Vender(models.Model):
    user = models.OneToOneField("user.User", models.CASCADE)