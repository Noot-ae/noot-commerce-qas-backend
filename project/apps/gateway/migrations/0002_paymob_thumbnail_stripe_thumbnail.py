# Generated by Django 4.1.7 on 2023-07-31 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gateway', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymob',
            name='thumbnail',
            field=models.URLField(null=True),
        ),
        migrations.AddField(
            model_name='stripe',
            name='thumbnail',
            field=models.URLField(null=True),
        ),
    ]