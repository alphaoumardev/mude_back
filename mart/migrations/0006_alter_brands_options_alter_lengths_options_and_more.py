# Generated by Django 4.1.3 on 2022-11-24 03:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mart', '0005_alter_images_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='brands',
            options={'verbose_name_plural': 'Brands'},
        ),
        migrations.AlterModelOptions(
            name='lengths',
            options={'verbose_name_plural': 'Lengths'},
        ),
        migrations.AlterModelOptions(
            name='materials',
            options={'verbose_name_plural': 'Matrials'},
        ),
        migrations.AlterModelOptions(
            name='occasion',
            options={'verbose_name_plural': 'Occasions'},
        ),
    ]