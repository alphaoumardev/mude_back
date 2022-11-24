from django.contrib import admin
from orders.models import Wishlist, CartItem, Order, OrderItem, Coupon, Refund, Payments, ShippingAddress

admin.site.register(Wishlist)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)

admin.site.register(Coupon)
admin.site.register(Refund)
admin.site.register(Payments)
admin.site.register(ShippingAddress)
