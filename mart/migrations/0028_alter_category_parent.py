# Generated by Django 4.1.4 on 2022-12-22 03:03

from django.db import migrations
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mart', '0027_delete_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcates', to='mart.category'),
        ),
    ]
