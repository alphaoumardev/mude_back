# Generated by Django 4.1.3 on 2022-11-23 07:50

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_order_order_reference'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_reference',
            field=models.UUIDField(default=uuid.UUID('55a91e2c-d71a-4271-a459-ae4e2117c66e')),
        ),
    ]