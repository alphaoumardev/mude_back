# Generated by Django 4.1.4 on 2022-12-21 05:08

from django.db import migrations
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mart', '0023_alter_category_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='categorys',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='articles', to='mart.category'),
        ),
    ]
