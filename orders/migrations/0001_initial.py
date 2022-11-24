# Generated by Django 4.1.3 on 2022-11-23 06:36

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mart', '0001_initial'),
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.DecimalField(decimal_places=2, max_digits=6, null=True)),
                ('quantity', models.IntegerField(default=1)),
                ('size', models.CharField(max_length=20, null=True)),
                ('paid', models.BooleanField(default=False)),
                ('color', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mart.colorsoption')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mart.product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='customers.customerprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_reference', models.UUIDField(default=uuid.UUID('8f33c6af-414c-4345-bced-2c02d77028e8'))),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6, null=True)),
                ('status', models.CharField(choices=[('pending', 'pending'), ('Completed', 'completed')], default='pending', max_length=20)),
                ('checked_out', models.BooleanField(default=False)),
                ('isPaid', models.BooleanField(default=False)),
                ('paid_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('isDelivered', models.BooleanField(default=False)),
                ('delivered_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('isReceived', models.BooleanField(default=False)),
                ('refund_requested', models.BooleanField(default=False)),
                ('isRefunded', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mart.product')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customers.customerprofile')),
            ],
        ),
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=20, null=True)),
                ('state', models.CharField(blank=True, max_length=20, null=True)),
                ('city', models.CharField(blank=True, max_length=20, null=True)),
                ('zip', models.CharField(max_length=10, null=True)),
                ('street', models.CharField(max_length=100, null=True)),
                ('details', models.CharField(blank=True, max_length=200, null=True)),
                ('order_note', models.CharField(blank=True, max_length=200, null=True)),
                ('primary', models.BooleanField(default=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customers.customerprofile')),
            ],
            options={
                'verbose_name_plural': 'Addresses',
            },
        ),
        migrations.CreateModel(
            name='Refund',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField()),
                ('accepted', models.BooleanField(default=False)),
                ('email', models.EmailField(max_length=254)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order')),
            ],
        ),
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.CharField(blank=True, max_length=50, null=True)),
                ('total_amount', models.DecimalField(decimal_places=3, max_digits=6, null=True)),
                ('provider', models.CharField(max_length=20, null=True)),
                ('paid_at', models.DateTimeField(auto_now_add=True)),
                ('order', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.order')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customers.customerprofile')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.DecimalField(decimal_places=2, max_digits=6, null=True)),
                ('quantity', models.IntegerField(default=1)),
                ('color', models.CharField(max_length=20, null=True)),
                ('size', models.CharField(max_length=20, null=True)),
                ('product', models.ManyToManyField(blank=True, to='mart.product')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.shippingaddress'),
        ),
        migrations.AddField(
            model_name='order',
            name='cart',
            field=models.ManyToManyField(blank=True, to='orders.cartitem'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.customerprofile'),
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=15)),
                ('amount', models.FloatField()),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('expired_at', models.DateTimeField(auto_now=True)),
                ('order', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.order')),
            ],
        ),
    ]
