# Generated by Django 4.1.4 on 2023-01-13 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0003_contactus'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerprofile',
            name='nickname',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
