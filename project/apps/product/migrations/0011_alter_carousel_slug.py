# Generated by Django 4.1.7 on 2023-08-22 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_remove_banner_button_text_banner_button_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carousel',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
