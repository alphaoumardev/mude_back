from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from mart.models import Product, Category
from mart.serializers import CategorySerializer, ProductSerializer

"""USING MPTT MODEL"""


@api_view(["GET"])
@permission_classes([AllowAny])
def get_mptt_categories(request):
    if request.method == "GET":
        category = Category.objects.filter(parent=None)
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data)


class MyPageNumberPagination(PageNumberPagination):
    page_size = 8  # default page size
    page_size_query_param = 'size'  # ?page=xx&size=??

    def get_paginated_response(self, data):
        return Response({
            'page_size': self.page_size,
            'current_page_number': self.page.number,
            'total_pages': self.page.paginator.num_pages,
            'total_products': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })


class FilterProductByCategory(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('id').reverse()
    serializer_class = ProductSerializer
    pagination_class = MyPageNumberPagination

    def get_queryset(self):
        queryset = self.queryset
        category = self.request.query_params.get('category', None)
        if category is not None:
            category = get_object_or_404(Category, pk=category)
            queryset = queryset.filter(category__in=category.get_descendants(include_self=True))
        return queryset


"""USING THE RECURSIVE MODEL"""


@api_view(["GET"])
@permission_classes([AllowAny])
def get_by_parent_cate(request, parent):
    if request.method == "GET":
        categories = Category.objects.filter(parent=None, name=parent)
        try:
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(str(e), status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_by_subcate_second_cate(request, parent, second):
    if request.method == "GET":
        categories = Category.objects.filter(Q(parent__parent__name=parent) & Q(parent__name=second))
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_by_subcates_third_cate(request, parent, second, third):  # ap="blue"
    if request.method == "GET":
        categories = Category.objects.filter(Q(parent__parent__name=parent) &
                                             Q(parent__name=second) &
                                             Q(name=third))
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_by_subcates_third_variants(request, parent, second, third, color):  # ap="blue"
    if request.method == "GET":
        categories = Category.objects.filter(Q(parent__parent__name=parent) &
                                             Q(parent__name=second) &
                                             Q(name=third) &
                                             Q(article__brand_id=color))
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def get_product_by_parent(request, parent, second, third,
                          variant=None,
                          # brand=None,
                          # size=None, tag=None,
                          # length=None, material=None, occasion=None
                          ):
    if variant is None:
        variant = []
    # color = request.

    if request.method == "GET":
        category = Category.objects.filter(Q(parent__parent__name=parent) &
                                           Q(parent__name=second) &
                                           Q(name=third)).first()

        items = Product.objects.filter(Q(category=category), (
                Q(color__color_name=variant) |
                Q(brand__brand_name=variant) |
                Q(size__size_name=variant) |
                Q(tag__tag_name=variant) |
                Q(lengths__length_name=variant) |
                Q(materials__material_name=variant) |
                Q(occasion__occasion_name=variant)
        ))
        serializer = ProductSerializer(items, many=True)
        return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_product_by_parent_cate(request, parent):
    if request.method == "GET":
        category = Category.objects.filter(parent__parent__name=parent).first()
        products = Product.objects.filter(category=category)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_product_by_parent_second_cate(request, parent, second):
    if request.method == "GET":
        """None"""
        categorys = Category.objects.filter(parent__name=parent, name=second).first()

        # print(categorys)
        category = Category.objects.filter(name=categorys.name).first()
        print(category.name)
        products = Product.objects.filter(category=category).prefetch_related().select_related()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_product_by_third_cate(request, third):
    if request.method == "GET":
        category = Category.objects.get(id=third)
        print(category)
        products = Product.objects.filter(category=category)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


def get_queryset(self):
    queryset = self.queryset
    category = self.request.query_params.get('category', None)
    if category is not None:
        category_qs = Category.objects.filter(name=category)
        if category_qs.exists():
            category = category_qs.first()
            queryset = queryset.filter(
                Q(category_id__lft__gte=category.lft, category_id__rght__lte=category.rght) |
                Q(category_id__parent__lft__gte=category.lft, category_id__parent__rght__lte=category.rght) |
                Q(category_id__parent__parent__lft__gte=category.lft,
                  category_id__parent__parent__rght__lte=category.rght)
            )
    return queryset


def get_querysets(self):
    queryset = self.queryset
    first = self.request.query_params.get('first', None)
    second = self.request.query_params.get('second', None)
    third = self.request.query_params.get('third', None)

    if first is not None:
        queryset = queryset.filter(category__level=0, category_name=first)
    if second is not None:
        queryset = queryset.filter(Q(category__level=1) & Q(category__parent_name=first),
                                   category_name=second)
    if third is not None:
        queryset = queryset.filter(Q(category__level=2) & Q(category__parent_name=second),
                                   category_name=third)
    return queryset
