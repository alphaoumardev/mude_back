from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ParseError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from mart.models import Images
from mart.serializers import ProductSerializer


# Create your views here.
# Here are just for the products
@api_view(['POST'])
@permission_classes([AllowAny])
def post_new_product(request):
    if request.method == 'POST':
        try:
            seriliazer = ProductSerializer(data=request.data)
            if seriliazer.is_valid():
                # images = ImageSerializer(data=request.data['images'])
                seriliazer.save()
                # try:
                # images = request.data['image']
                # Images.objects.create(product=seriliazer, image=images)
                # except KeyError:
                #     raise ParseError('Request has no resource images attached')
                return Response(seriliazer.data)
            return Response(seriliazer.errors)
        except Exception as e:
            return Response('{} Order does not exist'.format(e), status=status.HTTP_400_BAD_REQUEST)
