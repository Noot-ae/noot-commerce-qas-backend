from django.db import models

# Create your models here.
class Tax(models.Model):
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField()
    to_date = models.DateTimeField()