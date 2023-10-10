# Generated by Django 4.1.7 on 2023-08-28 08:30

from django.db import migrations
import phonenumber_field.modelfields
from tenants.models import Client
from user.models import UserPhone

class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_region_parent_region'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userphone',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True),
        ),
    ]