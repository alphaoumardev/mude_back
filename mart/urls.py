from django.urls import path

from .product_filter import get_by_parent_cate, get_all_categories, get_by_subcates_third_cate, \
    get_by_subcate_second_cate
from .views import *

urlpatterns = [
    path('catenames/', get_all_categories, name='details'),

    path('catenames/<str:name>/', get_product_by_parent, name='parentd'),

    path('products-filters/', get_variations_filter, name="products-filters"),

    path('products-by-page/', ArticleViewSet.as_view({"get": "list"}), name='product'),
    path('all-products/', get_products, name='product'),

    path('single-product/<str:pk>', get_one_product, name='one'),
    path('single-product-by-category/<str:pk>', get_pro_by_category, name='pro'),

    path('new-products/', get_new_products, name="new_products"),
    path('onsale/', get_onsale_products, name="onsale"),

    path('cates/by-parent/<str:parent>/', get_by_parent_cate, name="by-parent"),
    path('cates/by-parent/<str:parent>/<str:second>/', get_by_subcate_second_cate, name="by-parent_second"),
    path('cates/by-parent/<str:parent>/<str:second>/<str:third>/', get_by_subcates_third_cate, name="by-parent-third"),
]
