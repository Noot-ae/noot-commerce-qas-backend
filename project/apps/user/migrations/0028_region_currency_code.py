# Generated by Django 4.1.7 on 2023-10-03 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0027_alter_shipmentprofile_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='region',
            name='currency_code',
            field=models.CharField(default='egp', max_length=16),
            preserve_default=False,
        ),
    ]
