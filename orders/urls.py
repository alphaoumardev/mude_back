from django.urls import path

from .views import *

urlpatterns = [

    path('cart/', create_cart, name='cart'),
    path('cart/<str:pk>', CartItemView.as_view(), name='cart_items'),

    path('wishlist/', create_wishlist, name='wishlist'),
    path('wishlist/<str:pk>', operate_wishlist, name='wishlist'),

    path('address/', create_address,  name='address'),
    path('orders/', create_order, name='orders'),
    path('orderitem/<str:pk>', create_order_item, name='orderItem'),

    path('orders/', get_orders, name='get_orders'),
    path('orders/myorder/', get_my_orders, name='get_my_orders'),

    path('post-review/', post_review_product, name="reviews"),


    path('orders/<str:pk>/', get_order_by_id, name='get_order_by_id'),
    path('orders/<str:pk>/deliver/', update_order_to_delivered, name='update_order_to_delivered'),
    path('orders/<str:pk>/pay/', update_order_to_paid, name='update_order_to_paid'),
]
