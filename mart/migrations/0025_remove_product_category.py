# Generated by Django 4.1.4 on 2022-12-21 05:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mart', '0024_product_categorys'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
    ]