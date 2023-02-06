from django.urls import path

from .views import *

urlpatterns = [
    path('add-products/', post_new_product, name='post_new_product'),
    path('add-products/', ImageCreateView.as_view(), name='post_new_product'),
]
