# Generated by Django 4.1.7 on 2023-08-22 13:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_productbanner_sub_title_productbanner_title_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProductBanner',
        ),
    ]