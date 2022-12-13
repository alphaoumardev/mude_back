from customers.serializers import CustomerProfileSerializer
from mart.models import Reviews
from mart.serializers import ProductSerializer
from rest_framework import serializers

from orders.models import ShippingAddress, Wishlist, Coupon, OrderItem, Order, Payments, Refund, CartItem


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'



class ShippingAddressReadSerializer(serializers.ModelSerializer):
    cutomer = CustomerProfileSerializer(read_only=True)

    class Meta:
        model = ShippingAddress
        fields = '__all__'
        depth = 1


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = '__all__'


class WishlistReadSerializer(serializers.ModelSerializer):
    # product = ProductSerializer(required=False, read_only=True)
    # customer = CustomerProfileSerializer(required=False, read_only=True)

    class Meta:
        model = Wishlist
        fields = '__all__'
        depth = 1


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'
        # depth = 1


class CartItemReadSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True,)
    # customer = CustomerProfileSerializer(read_only=True,)

    class Meta:
        model = CartItem
        fields = '__all__'
        depth = 1


class CartItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderItemReadSerializer(serializers.ModelSerializer):
    # product = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = OrderItem
        fields = '__all__'
        depth = 1

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderReadSerializer(serializers.ModelSerializer):
    customer = CustomerProfileSerializer(required=False, read_only=True)
    address = ShippingAddressReadSerializer(required=False, read_only=True)
    cart = CartItemReadSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        # depth = 4


class PaymentDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'


class RefundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refund
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = '__all__'
