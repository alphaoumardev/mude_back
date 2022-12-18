from django.urls import path

from .views import *


urlpatterns = [
    path('catenames/', get_all_categories, name='details'),
    path('catenames/<str:name>/', get_product_by_parent, name='parentd'),
    path('catenames/<str:parent>/<str:name>/<str:subcate>/', get_product_by_category, name='pro'),

    path('products-filters/', get_variations_filter, name="products-filters"),

    path('products-by-page/', ArticleViewSet.as_view({"get": "list"}), name='product'),
    path('all-products/', get_products, name='product'),

    path('single-product/<str:pk>', get_one_product, name='one'),
    path('single-product-by-category/<str:pk>', get_pro_by_category, name='pro'),

    path('new-products/', get_new_products, name="new_products"),
    path('onsale/', get_onsale_products, name="onsale"),

]
