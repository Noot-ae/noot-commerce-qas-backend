# Generated by Django 4.1.7 on 2023-08-22 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('translations', '0001_initial'),
        ('product', '0009_carousel_banner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='banner',
            name='button_text',
        ),
        migrations.AddField(
            model_name='banner',
            name='button_text',
            field=models.ManyToManyField(blank=True, related_name='product_button_text_set', to='translations.translation'),
        ),
    ]
