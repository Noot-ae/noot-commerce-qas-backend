# Generated by Django 4.1.7 on 2023-07-31 08:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gateway', '0002_paymob_thumbnail_stripe_thumbnail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymob',
            name='thumbnail',
        ),
        migrations.RemoveField(
            model_name='stripe',
            name='thumbnail',
        ),
    ]
