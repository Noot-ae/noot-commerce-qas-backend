# Generated by Django 4.1.7 on 2023-09-25 13:36

from django.db import migrations
import utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0024_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=utils.fields.LimitedImageField(blank=True, null=True, upload_to=''),
        ),
    ]