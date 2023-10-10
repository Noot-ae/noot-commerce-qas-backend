# Generated by Django 4.1.7 on 2023-09-25 11:59

from django.db import migrations, models
import django.db.models.deletion
import product.models.variant_images
import utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('translations', '0002_alter_translation_text'),
        ('product', '0025_product_is_ratable_alter_banner_product_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='product_image',
            field=utils.fields.LimitedImageField(blank=True, null=True, upload_to='', validators=[utils.fields.LimitedImageField.validate_max_size, utils.fields.LimitedImageField.validate_max_size]),
        ),
        migrations.AlterField(
            model_name='banner',
            name='thumbnail',
            field=utils.fields.LimitedImageField(blank=True, null=True, upload_to='', validators=[utils.fields.LimitedImageField.validate_max_size, utils.fields.LimitedImageField.validate_max_size]),
        ),
        migrations.AlterField(
            model_name='product',
            name='display_image',
            field=utils.fields.LimitedImageField(null=True, upload_to='', validators=[utils.fields.LimitedImageField.validate_max_size, utils.fields.LimitedImageField.validate_max_size]),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=utils.fields.LimitedImageField(upload_to=product.models.variant_images.product_image_handler, validators=[utils.fields.LimitedImageField.validate_max_size, utils.fields.LimitedImageField.validate_max_size]),
        ),
        migrations.CreateModel(
            name='ProductDescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('description', models.ManyToManyField(blank=True, related_name='product_section_description_translations_set', to='translations.translation')),
                ('name', models.ManyToManyField(blank=True, related_name='product_section_name_translations_set', to='translations.translation')),
                ('product', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_description_set', to='product.product')),
            ],
        ),
    ]