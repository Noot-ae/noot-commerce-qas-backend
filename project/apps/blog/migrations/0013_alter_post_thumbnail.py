# Generated by Django 4.1.7 on 2023-09-25 13:36

from django.db import migrations
import utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_alter_post_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='thumbnail',
            field=utils.fields.LimitedImageField(blank=True, null=True, upload_to=''),
        ),
    ]
