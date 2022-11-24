from customers.models import CustomerProfile
from customers.serializers import UserSerializer, RegisterSerializer, \
    ChangePasswordSerializer, CustomerProfileSerializer

from django.contrib.auth import login
from django.contrib.auth.models import User
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class RegisterAPI(generics.GenericAPIView):  # Register API
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        data = request.data
        username = data.get('username')
        email = data.get('email')
        serializer = self.get_serializer(data=data)
        users_qs = User.objects.filter(email=email)
        user_name = User.objects.filter(username=username)
        if users_qs.exists():
            return Response({'A user with this email already exists'})
        elif user_name.exists():
            return Response({'A user with this username already exists'})
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            CustomerProfile.objects.create(user=user)  # To create automatically a profile during registering
        except Exception as e:
            return Response({'detail': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, formats=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


class ChangePasswordView(generics.UpdateAPIView):  # To change the password
    serializer_class = ChangePasswordSerializer  # An endpoint for changing password.
    model = User
    permission_classes = (IsAuthenticated,)

    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.object = None

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):  # Check old password
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            self.object.set_password(serializer.data.get("new_password"))  # set_password hashes the password
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


@permission_classes([IsAuthenticated])
@api_view(['POST', 'PATCH', 'GET'])
def customer_profile(request):
    """
    :param request:
    :return:
    """
    if request.method == "POST":
        serializer = CustomerProfileSerializer(data=request.data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    if request.method == "GET":
        user = request.user
        profile = CustomerProfile.objects.filter(user=user)
        serializer = CustomerProfileSerializer(profile, many=True)
        return Response(serializer.data)

    if request.method == "PATCH":
        user = request.user.id
        customer = CustomerProfile.objects.get(id=user)
        seriliazer = CustomerProfileSerializer(instance=customer, data=request.data)
        if seriliazer.is_valid():
            seriliazer.save()
        return Response(seriliazer.data)
