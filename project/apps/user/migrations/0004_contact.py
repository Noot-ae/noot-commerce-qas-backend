# Generated by Django 4.1.7 on 2023-08-17 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_shipmentprofile_city'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(max_length=64)),
                ('email', models.EmailField(max_length=254)),
                ('subject', models.TextField(max_length=256)),
                ('message', models.TextField(max_length=2048)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
