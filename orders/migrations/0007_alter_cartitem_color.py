# Generated by Django 4.1.3 on 2022-12-10 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_rename_user_cartitem_customer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='color',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
