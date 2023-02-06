from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from mart.models import Images, Product
from mart.serializers import ProductSerializer, ImageSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def post_new_product(request):
    if request.method == 'POST':
        try:
            seriliazer = ProductSerializer(data=request.data)
            if seriliazer.is_valid():
                # images = ImageSerializer(data=request.data['images'])
                seriliazer.save()
                Product.objects.get(id=request.data['product'])
                # try:
                # images = request.data['image']
                Images.objects.create(product=seriliazer, image=request.data['image'])
                # except KeyError:
                #     raise ParseError('Request has no resource images attached')
                return Response(seriliazer.data)
            return Response(seriliazer.errors)
        except Exception as e:
            return Response('{} Order does not exist'.format(e), status=status.HTTP_400_BAD_REQUEST)


class ImageCreateView(generics.CreateAPIView):
    serializer_class = ImageSerializer

    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product')
        product = Product.objects.get(id=product_id)
        images = request.FILES.getlist('images')

        for image in images:
            Images.objects.create(product=product, image=image)

        return Response(status=status.HTTP_201_CREATED)
