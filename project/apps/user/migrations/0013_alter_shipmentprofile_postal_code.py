# Generated by Django 4.1.7 on 2023-09-20 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_otp_otp_type_alter_otp_otp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipmentprofile',
            name='postal_code',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
