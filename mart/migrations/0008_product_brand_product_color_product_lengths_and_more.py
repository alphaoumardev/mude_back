# Generated by Django 4.1.3 on 2022-11-24 03:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mart', '0007_remove_product_brand_remove_product_color_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mart.brands'),
        ),
        migrations.AddField(
            model_name='product',
            name='color',
            field=models.ManyToManyField(blank=True, related_name='colored', to='mart.colorsoption'),
        ),
        migrations.AddField(
            model_name='product',
            name='lengths',
            field=models.ManyToManyField(blank=True, related_name='lened', to='mart.lengths'),
        ),
        migrations.AddField(
            model_name='product',
            name='materials',
            field=models.ManyToManyField(blank=True, related_name='materialized', to='mart.materials'),
        ),
        migrations.AddField(
            model_name='product',
            name='occasion',
            field=models.ManyToManyField(blank=True, related_name='occusioned', to='mart.occasion'),
        ),
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.ManyToManyField(blank=True, related_name='sized', to='mart.sizesoption'),
        ),
        migrations.AddField(
            model_name='product',
            name='tag',
            field=models.ManyToManyField(blank=True, related_name='tagged', to='mart.tag'),
        ),
    ]
