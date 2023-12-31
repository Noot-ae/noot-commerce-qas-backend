# Generated by Django 4.1.7 on 2023-08-10 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenants', '0006_remove_client_currency_factor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='currency_name',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='client',
            name='currency_symbol',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
    ]
