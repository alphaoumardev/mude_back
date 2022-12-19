from mart.serializers import ReviewSerializer
from orders.models import *
from datetime import datetime
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from orders.serializers import CartItemSerializer, OrderSerializer, CartItemUpdateSerializer, \
    WishlistSerializer, WishlistReadSerializer, ShippingAddressSerializer, OrderReadSerializer, \
    CartItemReadSerializer, OrderItemReadSerializer, ShippingAddressReadSerializer, OrderItemSerializer


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def create_cart(request):
    """
    :param request:
    :return:
    """
    current_customer = CustomerProfile.objects.get(user_id=request.user.id)
    order_total = 0.0

    if request.method == 'GET':
        try:
            cart_items = CartItem.objects.filter(paid=False, customer=current_customer).order_by('id').reverse()
            cart_count = cart_items.count()
            serializer = CartItemReadSerializer(cart_items, many=True)

            for item in cart_items:
                if item is not None:
                    order_total += float(item.total)

            return Response(
                {
                    "result": serializer.data,
                    "order_total": order_total,
                    "cart_count": cart_count,
                })
        except Exception as e:
            return Response({"message": '{}'.format(e), }, status=status.HTTP_204_NO_CONTENT)

    if request.method == "POST":
        try:
            serializer = CartItemSerializer(data=request.data, many=False)
            product = Product.objects.get(id=request.data['product'])
            check_item = CartItem.objects.filter(product_id=product, paid=False).exists()

            if check_item:
                update_data = CartItem.objects.get(product_id=product)
                serializer = CartItemSerializer(instance=update_data, data=request.data, many=False)

                if serializer.is_valid():
                    serializer.save()

                    product = Product.objects.get(id=request.data['product'])
                    quantity = int(request.data['quantity'])
                    cart_item = get_object_or_404(CartItem, product=product, paid=False)

                    product.stock -= quantity
                    product.save()
                    cart_item.total = float(product.price) * quantity
                    cart_item.customer = current_customer
                    cart_item.save()
                    return Response(serializer.data)
                return Response(serializer.errors)

            if serializer.is_valid():
                serializer.save()

                product = Product.objects.get(id=request.data['product'])
                quantity = int(request.data['quantity'])
                cart_item = get_object_or_404(CartItem, product=product, paid=False)

                product.stock -= quantity
                product.save()
                cart_item.total = float(product.price) * quantity
                cart_item.customer = current_customer
                cart_item.save()
                return Response(serializer.data)
        except Exception as e:
            return Response({"message": '{}'.format(e), }, status=status.HTTP_204_NO_CONTENT)


class CartItemView(RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()

    def retrieve(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            current_customer = CustomerProfile.objects.get(user=request.user)

            cart_item = self.get_object()
            if cart_item.customer != current_customer:
                raise PermissionDenied("Access Denied")
            serializer = self.get_serializer(cart_item)
            return Response(serializer.data)
        except Exception as e:
            return Response({"message": '{}'.format(e), }, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            current_customer = CustomerProfile.objects.get(user=request.user)

            cart_item = self.get_object()
            product = get_object_or_404(Product, pk=request.data['product'])

            if cart_item.customer != current_customer:
                raise PermissionDenied("This cart don't belong to you")

            quantity = int(request.data['quantity'])

            if quantity > product.stock:
                return Response("This product is out of stock")

            total = float(product.price) * quantity
            cart_item.total = total
            cart_item.customer = current_customer
            cart_item.save()
            product.stock -= quantity
            product.save()
            serializer = CartItemUpdateSerializer(cart_item, data=request.data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)
        except Exception as e:
            return Response({"message": '{}'.format(e), }, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        current_customer = CustomerProfile.objects.get(user=request.user)
        cart_item = self.get_object()
        if cart_item.customer != current_customer:
            raise PermissionDenied("Access Denied")
        cart_item.delete()
        return Response("You have successfully deleted your cart item", status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def create_wishlist(request, ):
    """
    :param request:
    :return:
    """
    current_customer = CustomerProfile.objects.get(user=request.user)

    if request.method == 'GET':
        wishlist = Wishlist.objects.filter(customer=current_customer).order_by('-id')
        wishlist_count = wishlist.count()
        serializer = WishlistReadSerializer(wishlist, many=True)
        return Response({"result": serializer.data, "wishlist_count": wishlist_count, })

    if request.method == "POST":
        try:
            serializer = WishlistSerializer(data=request.data, many=False, )

            product = Product.objects.get(id=request.data['product'])
            check_item = Wishlist.objects.filter(product_id=product).exists()

            if check_item:
                updated_data = Wishlist.objects.get(product_id=product)
                serializer = WishlistSerializer(instance=updated_data, data=request.data)

                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        except Exception as e:
            return Response({"message": '{}'.format(e)}, status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def operate_wishlist(request, pk):
    """
    :param request:
    :param pk:
    :return:
    """
    current_customer = CustomerProfile.objects.get(user=request.user)

    if request.method == 'GET':
        wishlist = Wishlist.objects.get(id=pk, customer=current_customer)
        serializer = WishlistReadSerializer(wishlist, many=False)
        # check_item = Wishlist.objects.filter(product_id=product).exists()

        return Response(serializer.data)

    if request.method == 'PUT':
        try:
            wishlist_item = Wishlist.objects.get(id=pk)
            serializer = WishlistSerializer(instance=wishlist_item, data=request.data, )
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)
        except Exception as e:
            return Response({"message": '{}'.format(e)}, status=status.HTTP_204_NO_CONTENT)

    if request.method == 'DELETE':
        try:
            wishlist_item = Wishlist.objects.get(id=pk)
            wishlist_item.delete()
            return Response("The wishlist item is deleted")
        except Exception as e:
            return Response({"message": '{}'.format(e)}, status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def create_address(request, ):
    """
    :param request:
    :return:
    """
    current_customer = CustomerProfile.objects.get(user=request.user)

    if request.method == 'GET':
        try:
            shipping_address = ShippingAddress.objects.filter(customer=current_customer).first()
            serializer = ShippingAddressReadSerializer(shipping_address, many=False)
            return Response(serializer.data)
        except Exception as e:
            return Response({"message": '{}'.format(e)}, status=status.HTTP_204_NO_CONTENT)

    if request.method == "POST":
        try:
            serializer = ShippingAddressSerializer(data=request.data, many=False, )

            customer_address = CustomerProfile.objects.get(id=request.data['customer'])
            check_address = ShippingAddress.objects.filter(customer_id=customer_address).exists()

            if check_address:
                updated_address = ShippingAddress.objects.get(customer_id=customer_address)
                serializer = ShippingAddressSerializer(instance=updated_address, data=request.data)

                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        except Exception as e:
            return Response({"message": '{}'.format(e)}, status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_order_items(request, ):
    """
    :param request:
    :return:
    """
    current_customer = CustomerProfile.objects.get(user=request.user)

    try:
        if request.method == 'GET':
            order_item = OrderItem.objects.filter(customer=current_customer).order_by('-id')
            serializer = OrderItemReadSerializer(order_item, many=True)
            return Response(serializer.data)
    except Exception as e:
        return Response({"message": '{}'.format(e)}, status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def create_order(request, ):
    """
    :param request:
    :return:
    """
    current_customer = CustomerProfile.objects.get(user=request.user)

    try:
        if request.method == 'GET':
            orders = Order.objects.filter(customer=current_customer).order_by('paid_at').reverse()
            serializer = OrderReadSerializer(orders, many=True)
            return Response(serializer.data)
    except Exception as e:
        return Response({"message": '{}'.format(e)}, status=status.HTTP_204_NO_CONTENT)

    if request.method == "POST":
        try:
            serializer = OrderSerializer(data=request.data, many=False)

            if serializer.is_valid():
                serializer.save()

                carts = CartItem.objects.filter(customer=current_customer, paid=False)
                order = Order.objects.filter(customer=current_customer).last()
                # all_my_orders = Order.objects.filter(customer=current_customer,)

                # for item_count in all_my_orders:
                #     order.order_items_count = item_count.count()
                #     order.save()

                for p in carts:
                    p.paid = True
                    p.save()
                order.status = "Processing"
                order.checked_out = True
                order.isPaid = True
                order.cart.set(carts)
                order.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        except Exception as e:
            return Response({"message": '{}'.format(e)}, status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def create_order_item(request, pk):
    """
    :param request:
    :param pk:
    :return:
    """
    if request.method == 'GET':
        try:
            # The order_item
            order_items = OrderItem.objects.filter(order=pk)
            orders_total = 0
            for item in order_items:
                orders_total += item.total
            serializer = OrderItemReadSerializer(order_items, many=True)
            return Response(
                {
                    "result": serializer.data,
                    "orders_total": orders_total,
                })
        except Exception as e:
            return Response({"message": '{}'.format(e)}, status=status.HTTP_204_NO_CONTENT)

    if request.method == "POST":
        try:

            current_customer = CustomerProfile.objects.get(user=request.user)

            serializer = OrderItemSerializer(data=request.data, many=False)

            if serializer.is_valid():
                serializer.save()

                order_products = CartItem.objects.filter(customer=current_customer)

                order_item = OrderItem.objects.get(order=pk)
                order_item.product.set(order_products)

                # product = Product.objects.get(id=request.data['product'])
                # quantity = int(request.data['quantity'])
                # order_item = get_object_or_404(OrderItem, product=product)
                # order_item.total=
                # product.stock -= quantity
                # product.save()
                # total = float(product.price) * quantity

                # order_item.total = total
                order_item.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        except Exception as e:
            return Response({"message": '{}'.format(e)}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_orders(request):
    """
    :param request:
    :return:
    """
    """HEEeee"""
    try:
        current_customer = CustomerProfile.objects.get(user=request.user)
        orders = current_customer.order_set.all()
        serializer = OrderReadSerializer(orders, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"message": '{}'.format(e)}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAdminUser])  # just the admin can monitor the whole orders
def get_orders(request):
    """
    :param request:
    :return:
    """
    try:
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"message": '{}'.format(e)}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order_by_id(request, pk):
    """
    :param request:
    :param pk:
    :return:
    """
    current_customer = CustomerProfile.objects.get(user=request.user)

    try:
        order = Order.objects.get(id=pk)
        if current_customer.is_staff or order.customer == current_customer:
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)
        else:
            return Response('Not authorized to view this order', status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response('{} Order does not exist'.format(e), status=status.HTTP_400_BAD_REQUEST)
    # finally:
    #     return Response("This order does not exist")


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_order_to_paid(request, pk):
    """
    :param request:
    :param pk:
    :return:
    """
    try:
        order = Order.objects.get(id=pk)
        order.isPaid = True
        order.paid_at = datetime.now()
        order.save()
        return Response('Order Purchased')
    except Exception as e:
        return Response({"message": '{}'.format(e)}, status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_order_to_delivered(request, pk):
    """
    :param request:
    :param pk:
    :return:
    """
    order = Order.objects.get(id=pk)
    order.isDelivered = True
    order.status = "Delivered"
    order.delivered_at = datetime.now()
    order.save()
    return Response('Order delivered')


class CartItemViews(APIView):
    @staticmethod
    def post(request):
        """
        :param request:
        :return:
        """
        try:
            serializer = CartItemSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({serializer.data}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"message": '{}'.format(e)}, status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def get(request, pk=None):
        """
        :param request:
        :param pk:
        :return:
        """
        if pk:
            item = CartItem.objects.get(id=pk)
            serializer = CartItemSerializer(item)
            return Response(serializer.data, status=status.HTTP_200_OK)

        item = CartItem.objects.all()
        serializer = CartItemSerializer(item, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def patch(request, pk=None):
        """
        :param request:
        :param pk:
        :return:
        """
        item = CartItem.objects.get(id=pk)
        serializer = CartItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({serializer.data})
        else:
            return Response(serializer.errors)

    @staticmethod
    def delete(request, pk=None):
        """
        :param request:
        :param pk:
        :return:
        """
        item = get_object_or_404(CartItem, pk=pk)
        item.delete()
        return Response({"Item Deleted"})


class CreateCartApiView(ListCreateAPIView):
    serializer_class = CartItemSerializer

    def get_queryset(self):
        """
        :return:
        """
        user = self.request.user
        queryset = CartItem.objects.filter(cart__user=user, )
        return queryset

    def create(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        user = request.user
        cart = get_object_or_404(CartItem, user=user)
        product = get_object_or_404(Product, pk=request.data['product'])
        color = get_object_or_404(CartItem, pk=request.data['color'])
        size = get_object_or_404(CartItem, pk=request.data['size'])

        # current_item = CartItem.objects.filter(cart=cart, product=product)
        quantity = int(request.data['quantity'])

        # if current_item.count() > 0:
        #     Response("You already have this product in your cart")

        if quantity > product.stock:
            return Response("There is no enough product in stock")
        # serializer = CartItemSerializer(data=request.data)
        cart_item = CartItem(cart=cart, product=product, quantity=quantity, color=color, size=size)
        # product.stock -= cart_item.quantity
        # cart_item.save()
        serializer = CartItemSerializer(cart_item)
        # if serializer.is_valid():
        serializer.save()
        # return Response(serializer.data)
        total = float(product.price) * quantity
        cart.total = total
        cart.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# class OrderView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request, pk, *args, **kwargs):
#         user = request.user
#         address = ShippingAddress.objects.filter(user=user, primary=True).first()
#         product = get_object_or_404(Product, pk=pk)
#         if product.stock == 0:
#             return Response("This product is out of stock")
#         try:
#             order_reference = request.data.get("order_reference", '')
#             quantity = request.data.get("quantity", 1)
#
#             total = quantity * product.price
#             order = Order().create_order(user, order_reference, status, address, checked_out=True,
#                                          isPaid=False, isDelivered=False,
#                                          paid_at=datetime.datetime.now(),
#                                          delivered_at=datetime.datetime.now(),
#                                          ordered_at=datetime.datetime.now(),
#                                          refund_requested=False,
#                                          isReceived=False,
#                                          isRefunded=False, )
#             order_item = OrderItem().create_order_item(order, product, quantity, total)
#             # serializer = OrderItemReadSerializer(order_item, )
#
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#         except Exception as e:
#             return Response("An error occur when creating the order", e)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_review_product(request):
    try:
        if request.method == "POST":
            serializer = ReviewSerializer(data=request.data, many=False)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
    except Exception as e:
        return Response({"message": '{}'.format(e)}, status=status.HTTP_204_NO_CONTENT)
