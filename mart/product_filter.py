from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from mart.models import Categories, Product
from mart.serializers import ByCategorySerializer, CategorySerializer, ProductSerializer


@api_view(["GET"])
@permission_classes([AllowAny])
def get_all_categories(request):
    if request.method == "GET":
        categories = Categories.objects.filter(parent=None)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_by_parent_cate(request, parent):
    if request.method == "GET":
        categories = Categories.objects.filter(parent=None, name=parent)
        try:
            serializer = ByCategorySerializer(categories, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(str(e), status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_by_subcate_second_cate(request, parent, second):
    if request.method == "GET":
        categories = Categories.objects.filter(Q(parent__parent__name=parent) & Q(parent__name=second))
        serializer = ByCategorySerializer(categories, many=True)
        return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_by_subcates_third_cate(request, parent, second, third):  # ap="blue"
    if request.method == "GET":
        categories = Categories.objects.filter(Q(parent__parent__name=parent) &
                                               Q(parent__name=second) &
                                               Q(name=third))
        serializer = ByCategorySerializer(categories, many=True)
        return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_by_subcates_third_variants(request, parent, second, third, color):  # ap="blue"
    if request.method == "GET":
        categories = Categories.objects.filter(Q(parent__parent__name=parent) &
                                               Q(parent__name=second) &
                                               Q(name=third) &
                                               Q(article__brand_id=color))
        serializer = ByCategorySerializer(categories, many=True)
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
        category = Categories.objects.filter(Q(parent__parent__name=parent) &
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
