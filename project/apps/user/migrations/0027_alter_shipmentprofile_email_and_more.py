# Generated by Django 4.1.7 on 2023-10-01 08:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0026_alter_userphone_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipmentprofile',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='shipmentprofile',
            name='phone_number',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='user.userphone'),
        ),
    ]
