# Generated by Django 4.1.7 on 2023-09-18 08:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0017_rename_variantattribute_attribute_and_more'),
        ('orders', '0005_alter_order_order_status_alter_order_payment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_item_set', to='orders.order'),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='product_variant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='as_order_item_set', to='product.productvariant'),
        ),
    ]
