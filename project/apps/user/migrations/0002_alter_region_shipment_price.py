# Generated by Django 4.1.7 on 2023-07-31 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='region',
            name='shipment_price',
            field=models.IntegerField(default=0),
        ),
    ]
