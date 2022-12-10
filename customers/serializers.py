from rest_framework import serializers
from django.contrib.auth.models import User

from customers.models import CustomerProfile


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        users_qs = User.objects.filter(email=data['email'])
        user_name = User.objects.filter(username=['username'])
        if users_qs.exists() or user_name.exists():
            raise serializers.ValidationError('A user with this email or username already exists')
        else:
            return data

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'],
                                        validated_data['email'],
                                        validated_data['password'], )
        return user


# Serializer for password change endpoint.
class ChangePasswordSerializer(serializers.Serializer, ):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class CustomerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False, read_only=True)

    class Meta:
        model = CustomerProfile
        fields = '__all__'
        # depth = 1


class CustomerProfilePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = '__all__'
