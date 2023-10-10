# Generated by Django 4.1.7 on 2023-07-27 07:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0001_initial'),
        ('translations', '0001_initial'),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductBanner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='')),
                ('slug', models.SlugField(unique=True)),
                ('content', models.ManyToManyField(blank=True, to='translations.translation')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='page.section')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
        ),
    ]