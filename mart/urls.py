from django.urls import path

from .product_filter import *
from .views import *

urlpatterns = [

    path('mptt-categories/', get_mptt_categories, name='mptts'),
    path('filter-products-by-category/', FilterProductByCategory.as_view({"get": "list"}), name="filter-products"),
    path('filter-products-by-variant/', ProductVariant.as_view({'get': 'list'}), name="filtering-variants"),

    path('products_variant-filters/', get_variations_filter, name="products-filters"),

    path('products-by-page/', ArticleViewSet.as_view({"get": "list"}), name='product'),
    path('products-by-category/', GetProductByCategory.as_view({"get": "list"}), name='product'),

    path('all-products/', get_products, name='product'),

    path('single-product/<str:pk>', SingleProduct.as_view(), name='one'),
    path('single-product-by-category/<str:pk>', get_pro_by_category, name='pro'),

    path('new-products/', get_new_products, name="new_products"),
    path('onsale/', get_onsale_products, name="onsale"),
    path('trending-products/', get_trending_products, name="trending"),

    path('cates/<str:parent>/', get_by_parent_cate, name="by-parent"),
    path('cates/<str:parent>/<str:second>/', get_by_subcate_second_cate, name="by-parent_second"),
    path('cates/<str:parent>/<str:second>/<str:third>/', get_by_subcates_third_cate, name="by-parent-third"),
    path('cates/<str:parent>/<str:second>/<str:third>/<str:variant>/', get_product_by_parent, name="by-pro"),

    path('pro/<str:parent>/', get_product_by_parent_cate, name="by-parent"),
    path('pro/<str:parent>/<str:second>/', get_product_by_parent_second_cate, name="by-second"),
    path('products/<str:third>/', get_product_by_third_cate, name="by-third"),
]
