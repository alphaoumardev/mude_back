from django.contrib.auth.models import User, AbstractUser
from django.db import models

from customers.models import CustomerProfile
from mart.models import Product, ColorsOption


class Wishlist(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.product.name


class ShippingAddress(models.Model):
    customer = models.OneToOneField(CustomerProfile, on_delete=models.CASCADE, null=True, blank=True)
    nickname = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=20, null=True)
    state = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=20, null=True, blank=True, )
    zip = models.CharField(max_length=10, null=True)
    street = models.CharField(max_length=100, null=True)
    details = models.CharField(max_length=200, null=True, blank=True)
    order_note = models.CharField(max_length=200, null=True, blank=True)

    primary = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return self.customer.user.username


class CartItem(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    total = models.DecimalField(decimal_places=2, max_digits=6, null=True, )
    quantity = models.IntegerField(default=1, blank=True, null=True)
    color = models.CharField(max_length=20, null=True)
    size = models.CharField(max_length=20, null=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.product.name


class OrderItem(models.Model):
    product = models.ManyToManyField(Product, blank=True)
    total = models.DecimalField(decimal_places=2, max_digits=6, null=True, )
    quantity = models.IntegerField(default=1)
    color = models.CharField(max_length=20, null=True, blank=True)
    size = models.CharField(max_length=20, null=True, blank=True)

    def order_count(self):
        return self.product.count()
    # def __str__(self):
    #     return self.product.name


class Order(models.Model):
    OrderPlaced = "Order Placed"
    Processing = "Processing"
    Shipped = "Shipped"
    Delivered = "Delivered"

    ORDER_STATUS = ((OrderPlaced, "Order Placed"),
                    (Processing, "Processing"),
                    (Shipped, "Shipped"),
                    (Delivered, "Delivered"))

    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    order_reference = models.BigIntegerField(blank=True, null=True, unique=True)
    amount = models.DecimalField(max_digits=6, decimal_places=2, null=True)

    address = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE, null=True)
    cart = models.ManyToManyField(CartItem, blank=True)

    status = models.CharField(max_length=20, choices=ORDER_STATUS, default=OrderPlaced)
    checked_out = models.BooleanField(default=False)
    isPaid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(auto_now_add=True, null=True)
    order_items_count = models.IntegerField(default=1)

    isDelivered = models.BooleanField(default=False)
    delivered_at = models.DateTimeField(auto_now_add=True, null=True)
    isReceived = models.BooleanField(default=False)

    refund_requested = models.BooleanField(default=False)
    isRefunded = models.BooleanField(default=False)

    def __str__(self):
        return self.status


class Payments(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, null=True, blank=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True, blank=True)
    payment_id = models.CharField(max_length=50, null=True, blank=True)
    total_amount = models.DecimalField(decimal_places=3, max_digits=6, null=True)
    provider = models.CharField(max_length=20, null=True)
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.provider


class Coupon(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True, blank=True)
    code = models.CharField(max_length=15)
    amount = models.FloatField()
    added_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()
