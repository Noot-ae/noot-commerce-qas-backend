# Generated by Django 4.1.7 on 2023-08-28 06:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0009_alter_menuitem_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='menu',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='menu_item_set', to='category.menu'),
        ),
    ]
