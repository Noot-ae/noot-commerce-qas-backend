# Generated by Django 4.1.7 on 2023-08-02 08:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_delete_region'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='transaction_id',
            field=models.CharField(default=120004522, max_length=256),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='refund',
            name='payment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='payment.payment'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='gateway',
            field=models.CharField(choices=[('PAYMOB', 'Paymob'), ('STRIPE', 'Stripe')], max_length=12),
        ),
    ]
