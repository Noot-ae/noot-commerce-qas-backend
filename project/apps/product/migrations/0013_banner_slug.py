# Generated by Django 4.1.7 on 2023-08-27 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0012_alter_banner_redirect_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='slug',
            field=models.SlugField(null=True),
        ),
    ]
