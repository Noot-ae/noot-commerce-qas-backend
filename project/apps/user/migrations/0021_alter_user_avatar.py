# Generated by Django 4.1.7 on 2023-09-25 11:01

from django.db import migrations
import utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0020_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=utils.fields.LimitedImageField(blank=True, null=True, upload_to='', validators=[utils.fields.LimitedImageField.validate_max_size, utils.fields.LimitedImageField.validate_max_size]),
        ),
    ]
