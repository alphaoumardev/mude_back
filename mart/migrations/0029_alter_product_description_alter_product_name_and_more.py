# Generated by Django 4.1.4 on 2023-02-02 11:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mart', '0028_alter_category_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.CreateModel(
            name='FuturedImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.ImageField(blank=True, null=True, upload_to='mudi')),
                ('color_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mart.colorsoption')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mart.product')),
            ],
            options={
                'verbose_name_plural': 'Detail Images',
            },
        ),
    ]
