# Generated by Django 4.1.4 on 2022-12-21 15:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mart', '0026_rename_categorys_product_category'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Categories',
        ),
    ]