from django.db import models


class Contact(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField()
    subject = models.TextField(max_length=256)
    message = models.TextField(max_length=2048)
    created_at = models.DateTimeField(auto_now_add=True)
