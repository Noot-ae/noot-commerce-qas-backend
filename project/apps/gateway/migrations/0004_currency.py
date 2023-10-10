# Generated by Django 4.1.7 on 2023-08-09 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gateway', '0003_remove_paymob_thumbnail_remove_stripe_thumbnail'),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency_name', models.CharField(max_length=16)),
                ('currency_code', models.CharField(max_length=16)),
                ('currency_symbol', models.CharField(max_length=16)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True, unique=True)),
            ],
        ),
    ]
