from django.urls import path

from .views import *


urlpatterns = [
    path('pages/', get_product, name='produc'),
    path('products/', ArticleViewSet.as_view({"get": "list"}), name='product'),

    path('all/', get_products, name='product'),
    path('one/<str:pk>', get_one_product, name='one'),
    path('probycategory/<str:pk>', get_pro_by_category, name='pro'),

    path('catename/<str:query>', get_category_by_name, name='details'),
    path('catename/<str:query>/<str:name>', get_product_by_category, name='pro'),

    path('newproducts/', get_new_products, name="new_products"),
    path('onsale/', get_onsale_products, name="onsale"),

    path('colors/', get_colors, name="colors"),
    path('sizes/', get_sizes, name="sizes"),
    path('tags/', get_tags, name="tags"),
    path('bycolor/', filter_by_color, name="bycolor"),
    path('bysize/', filter_by_size, name="bysize"),
    path('byprice/', filter_by_price, name="byprice"),

    path('review/', review_products, name="reviews")
]
