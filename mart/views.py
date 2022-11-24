# Create your views here.
from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from orders.serializers import ReviewSerializer
from mart.serializers import *


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


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by("id")
    serializer_class = ProductSerializer
    pagination_class = MyPageNumberPagination
    permission_classes = [AllowAny]


# Here are just for the products
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def get_products(request):
    if request.method == 'GET':
        # the product search
        query = request.GET.get('query') if request.GET.get('query') is not None else ''
        products = Product.objects.filter(
            Q(category__product__name__contains=query) |
            Q(category__product__name__exact=query)
        )
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        seriliazer = ProductSerializer(data=request.data)
        if seriliazer.is_valid():
            seriliazer.save()
            return Response(seriliazer.data)
        return Response(seriliazer.errors)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def get_product(request):
    if request.method == 'GET':
        products = Product.objects.all().order_by("id")
        pag = Paginator(object_list=products, per_page=8)
        pages = request.GET.get('page')
        result = pag.get_page(pages)
        serializer = ProductSerializer(result, many=True)
        return Response(serializer.data, )
    if request.method == 'POST':
        seriliazer = ProductSerializer(data=request.data)
        if seriliazer.is_valid():
            seriliazer.save()
            return Response(seriliazer.data)
        return Response(seriliazer.errors, )


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def get_one_product(request, pk):
    if request.method == "GET":
        article = Product.objects.get(id=pk)
        reveiws = Reviews.objects.filter(product=article)
        count = reveiws.count()
        seriliazer = ProductSerializer(article, many=False)
        rev = ReviewSerializer(reveiws, many=True)
        return Response({"pro": seriliazer.data, "rev": rev.data, "count": count})

    if request.method == 'PUT':
        article = Product.objects.get(id=pk)
        seriliazer = ProductSerializer(instance=article, data=request.data)
        if seriliazer.is_valid():
            seriliazer.save()
        return Response(seriliazer.data)
    if request.method == 'DELETE':
        article = Product.objects.get(id=pk)
        article.delete()
        return Response("The note is deleted")


@api_view(["GET"])
@permission_classes([AllowAny])
def get_pro_by_category(request, pk):
    if request.method == "GET":
        category = Categories.objects.get(id=pk)
        variant = Product.objects.filter(category=category).order_by('-id')
        serializer = ProductSerializer(variant, many=True)
        return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_category_by_name(request, query=None):
    if request.method == "GET":
        category = Categories.objects.filter(genre__genre_name=query)
        serializer = CategoriesSerializer(category, many=True)
        return Response(serializer.data)


@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def get_product_by_category(request, query=None, name=None):
    if request.method == "GET":
        genre = Categories.objects.filter(genre__genre_name=query).filter(type__type_name=name)
        items = Product.objects.filter(category__genre__category__in=genre).filter(category__type__category__in=genre)
        serializer = ProductSerializer(items, many=True)
        return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_new_products(request):
    if request.method == "GET":
        new_products = Product.objects.filter(onsale='New')
        items = ProductSerializer(new_products, many=True)
        return Response(items.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_onsale_products(request):
    if request.method == "GET":
        new_products = Product.objects.filter(onsale='Sale')
        items = ProductSerializer(new_products, many=True)
        return Response(items.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_colors(request):
    if request.method == "GET":
        colors = ColorsOption.objects.all()
        items = ColorsOptionSerializer(colors, many=True)
        return Response(items.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_sizes(request):
    if request.method == "GET":
        sizes = SizesOption.objects.all()
        items = SizeSerialiser(sizes, many=True)
        return Response(items.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_tags(request):
    if request.method == "GET":
        tags = Tag.objects.all()
        items = TagSerializer(tags, many=True)
        return Response(items.data)


# Filter by color
@api_view(["GET"])
@permission_classes([AllowAny])
def filter_by_color(request):
    if request.method == "GET":
        color = request.GET.get('color') if request.GET.get('color') is not None else ''
        products = Product.objects.filter(Q(futuredimages__color_name__color_name=color))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


# Filter product by size
@api_view(["GET"])
@permission_classes([AllowAny])
def filter_by_size(request):
    if request.method == "GET":
        size = request.GET.get('size') if request.GET.get('size') is not None else ''
        products = Product.objects.filter(Q(variant__size__size_name=size))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


# Filter product by Tags
@api_view(["GET"])
@permission_classes([AllowAny])
def filter_by_tag(request):
    if request.method == "GET":
        tag = request.GET.get('tag') if request.GET.get('tag') is not None else ''
        products = Product.objects.filter(Q(variant__tag=tag) |
                                          Q(variant__tag__tag_name=tag))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


# Filter product by Price
@api_view(["GET"])
@permission_classes([AllowAny])
def filter_by_price(request):
    if request.method == "GET":
        less_price = request.GET.get('less_price') if request.GET.get('less_price') is not None else None
        greater_price = request.GET.get('greater_price') if request.GET.get('greater_price') is not None else None
        # price = Product.objects.get('price')
        products = Product.objects.filter(price__gte=less_price,
                                          price__lte=greater_price)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def review_products(request):
    if request.method == "POST":
        serializer = ReviewSerializer(data=request.data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    if request.method == "GET":
        reviews = Reviews.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
