from customers.serializers import UserSerializer
from mart.models import Reviews
from mart.serializers import ProductSerializer
from rest_framework import serializers

from orders.models import ShippingAddress, Wishlist, Coupon, OrderItem, Order, Payments, Refund, CartItem


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'


class ShippingAddressReadSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ShippingAddress
        fields = '__all__'


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = '__all__'


class WishlistReadSerializer(serializers.ModelSerializer):
    product = ProductSerializer(required=False, read_only=True)
    user = UserSerializer(required=False, read_only=True)

    class Meta:
        model = Wishlist
        fields = '__all__'


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'


class CartItemReadSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True,)
    user = UserSerializer(read_only=True,)

    class Meta:
        model = CartItem
        fields = '__all__'


class CartItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderItemReadSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderReadSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False, read_only=True)
    address = ShippingAddressReadSerializer(required=False, read_only=True)
    cart = CartItemReadSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


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
