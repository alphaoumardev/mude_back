# Generated by Django 4.1.3 on 2022-11-24 03:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mart', '0006_alter_brands_options_alter_lengths_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='brand',
        ),
        migrations.RemoveField(
            model_name='product',
            name='color',
        ),
        migrations.RemoveField(
            model_name='product',
            name='lengths',
        ),
        migrations.RemoveField(
            model_name='product',
            name='materials',
        ),
        migrations.RemoveField(
            model_name='product',
            name='occasion',
        ),
        migrations.RemoveField(
            model_name='product',
            name='size',
        ),
        migrations.RemoveField(
            model_name='product',
            name='slide',
        ),
        migrations.RemoveField(
            model_name='product',
            name='tag',
        ),
    ]
