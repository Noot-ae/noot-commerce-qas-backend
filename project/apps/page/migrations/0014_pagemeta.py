# Generated by Django 4.1.7 on 2023-10-03 09:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0013_alter_section_thumbnail'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageMeta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keywords', models.CharField(blank=True, max_length=256, null=True)),
                ('description', models.CharField(blank=True, max_length=256, null=True)),
                ('title_tag', models.CharField(blank=True, max_length=256, null=True)),
                ('og_image', models.CharField(blank=True, max_length=256, null=True)),
                ('og_title', models.CharField(blank=True, max_length=256, null=True)),
                ('og_description', models.CharField(blank=True, max_length=256, null=True)),
                ('page', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='page_meta', to='page.section')),
            ],
        ),
    ]