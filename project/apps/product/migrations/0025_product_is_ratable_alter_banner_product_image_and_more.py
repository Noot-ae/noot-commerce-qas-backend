# Generated by Django 4.1.7 on 2023-09-25 11:01

from django.db import migrations, models
import product.models.variant_images
import utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0024_product_display_image_alter_banner_product_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_ratable',
            field=models.BooleanField(default=True),
        ),
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
    ]
