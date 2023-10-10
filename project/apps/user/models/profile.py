from django.db import models

# Create your models here.
class ShipmentProfile(models.Model):
    user = models.ForeignKey("user.User", models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=16)
    last_name = models.CharField(max_length=16)

    street = models.CharField(max_length=64, blank=True, null=True)
    building = models.CharField(max_length=12, blank=True, null=True)
    floor = models.CharField(max_length=12, blank=True, null=True)
    apartment = models.CharField(max_length=32, blank=True, null=True)
    address = models.CharField(max_length=128)
    address_note = models.CharField(max_length=512, blank=True, null=True)
    
    country = models.CharField(max_length=64, null=True, blank=False)
    region = models.ForeignKey("user.Region", models.CASCADE, blank=False)
    postal_code = models.IntegerField(null=True, blank=True)


    created_at = models.DateTimeField(auto_now_add=True)
    phone_number = models.OneToOneField('user.UserPhone', models.CASCADE)
    email = models.EmailField(unique=True)
    profile_name = models.CharField(max_length=32)
    

