# Generated by Django 4.1.7 on 2023-09-18 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_squashed_0010_alter_userphone_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipmentprofile',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.region'),
        ),
    ]
