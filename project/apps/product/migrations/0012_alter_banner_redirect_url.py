# Generated by Django 4.1.7 on 2023-08-27 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0011_alter_carousel_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='redirect_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]