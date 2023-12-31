# Generated by Django 4.1.7 on 2023-09-21 13:13

import category.models.category
from django.db import migrations
import utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0012_alter_menuitem_page'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='thumbnail',
            field=utils.fields.LimitedImageField(blank=True, null=True, upload_to=category.models.category.category_img_handler),
        ),
    ]
