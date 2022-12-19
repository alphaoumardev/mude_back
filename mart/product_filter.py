from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from mart.models import Categories
from mart.serializers import ByCategorySerializer, CategorySerializer


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
        serializer = ByCategorySerializer(categories, many=True)
        return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_by_subcate_second_cate(request, parent, second):
    if request.method == "GET":
        categories = Categories.objects.filter(parent__name=parent, name=second)
        serializer = ByCategorySerializer(categories, many=True)
        return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_by_subcates_third_cate(request, parent, second, third):
    if request.method == "GET":
        categories = Categories.objects.filter(parent__parent__name=parent, parent__name=second, name=third)
        serializer = ByCategorySerializer(categories, many=True)
        return Response(serializer.data)
