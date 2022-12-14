# Generated by Django 4.1.3 on 2022-12-19 06:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mart', '0017_alter_genre_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article', to='mart.categories'),
        ),
        migrations.CreateModel(
            name='Taga',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('taga_name', models.CharField(blank=True, max_length=15, null=True, unique=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='taigao', to='mart.genre')),
            ],
        ),
    ]
