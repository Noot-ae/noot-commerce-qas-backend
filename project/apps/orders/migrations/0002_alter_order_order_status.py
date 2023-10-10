# Generated by Django 4.1.7 on 2023-08-02 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('PLACED', 'Placed'), ('SHIPPED', 'Shipped'), ('RECEIVED', 'Received'), ('CANCELLED', 'Cancelled')], default='PLACED', max_length=32),
        ),
    ]