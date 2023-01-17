from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from mart.models import Category, Product, ColorsOption, \
    Tag, SizesOption, Materials, Occasion, Brands, Lengths, Reviews

from mart.serializers import ProductSerializer, ColorsOptionSerializer, TagSerializer, \
    SizeSerialiser, MaterialSerializer, OccasionSerializer, \
    BrandSerializer, LengthSerializer, ReviewReadSerializer

"""To Jenny"""


print('\n'.join
      ([''.join
        ([('Jenny'[(x - y) % 5]
           if ((x * 0.05) ** 2 + (y * 0.1) ** 2 - 1)
              ** 3 - (x * 0.05) ** 2 * (y * 0.1)
              ** 3 <= 0 else ' ')
          for x in range(-30, 30)])
        for y in range(15, -15, -1)]))


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
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = MyPageNumberPagination
    permission_classes = [AllowAny]


class GetProductByCategory(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = MyPageNumberPagination
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = self.queryset
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category_id=category)
        return queryset


class SingleProduct(APIView):
    lookup_field = "pk"
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    @staticmethod
    def get_object(pk):
        try:
            return Product.objects.get(id=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk, ):
        article = self.get_object(pk)
        serializer = ProductSerializer(article)
        return Response(serializer.data)


@api_view(["GET", ])
@permission_classes([AllowAny])
def get_variations_filter(request):
    """To get the variations to filter products"""
    if request.method == "GET":
        try:
            colors = ColorsOption.objects.all()
            color_serializer = ColorsOptionSerializer(colors, many=True)

            tags = Tag.objects.all()
            tag_serializer = TagSerializer(tags, many=True)

            sizes = SizesOption.objects.all()
            size_serializer = SizeSerialiser(sizes, many=True)

            materials = Materials.objects.all()
            mate_serializer = MaterialSerializer(materials, many=True)

            occasions = Occasion.objects.all()
            occ_serializer = OccasionSerializer(occasions, many=True)

            brands = Brands.objects.all()
            brand_serializer = BrandSerializer(brands, many=True)

            lengths = Lengths.objects.all()
            length_serializer = LengthSerializer(lengths, many=True)

            return Response({
                "colors": color_serializer.data,
                "tags": tag_serializer.data,
                "sizes": size_serializer.data,
                "materials": mate_serializer.data,
                "occasions": occ_serializer.data,
                "brands": brand_serializer.data,
                "lengths": length_serializer.data
            })
        except Exception as e:
            return Response({"message": '{}'.format(e)}, status=status.HTTP_204_NO_CONTENT)


# Here are just for the products
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def get_products(request):
    if request.method == 'GET':
        # the product search
        query = request.GET.get('query') if request.GET.get('query') is not None else ''
        # products = Product.objects.all()
        serializer = ProductSerializer(query, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        seriliazer = ProductSerializer(data=request.data)
        if seriliazer.is_valid():
            seriliazer.save()
            return Response(seriliazer.data)
        return Response(seriliazer.errors)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def get_one_product(request, pk):
    if request.method == "GET":
        article = Product.objects.get(id=pk)
        reveiws = Reviews.objects.filter(product=article).order_by('reviewed_at').reverse()
        count = reveiws.count()
        seriliazer = ProductSerializer(article, many=False)
        rev = ReviewReadSerializer(reveiws, many=True)
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
def get_trending_products(request):
    if request.method == "GET":
        trending = Product.objects.filter(onsale='Sale')[:6]
        items = ProductSerializer(trending, many=True)
        return Response(items.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_pro_by_category(request, pk):
    if request.method == "GET":
        category = Category.objects.get(id=pk)
        variant = Product.objects.filter(category=category).order_by('-id')
        serializer = ProductSerializer(variant, many=True)
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
