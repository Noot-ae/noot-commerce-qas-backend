# Generated by Django 4.1.7 on 2023-09-24 13:31

from django.db import migrations
import utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_alter_post_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='thumbnail',
            field=utils.fields.LimitedImageField(blank=True, null=True, upload_to='', validators=[utils.fields.LimitedImageField.validate_max_size, utils.fields.LimitedImageField.validate_max_size]),
        ),
    ]