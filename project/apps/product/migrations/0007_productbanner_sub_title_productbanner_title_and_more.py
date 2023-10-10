# Generated by Django 4.1.7 on 2023-08-22 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('translations', '0001_initial'),
        ('product', '0006_productbanner_button_text_productbanner_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='productbanner',
            name='sub_title',
            field=models.ManyToManyField(blank=True, related_name='product_banner_sub_title_set', to='translations.translation'),
        ),
        migrations.AddField(
            model_name='productbanner',
            name='title',
            field=models.ManyToManyField(blank=True, related_name='product_banner_title_set', to='translations.translation'),
        ),
        migrations.AlterField(
            model_name='productbanner',
            name='content',
            field=models.ManyToManyField(blank=True, related_name='product_banner_content_set', to='translations.translation'),
        ),
    ]
