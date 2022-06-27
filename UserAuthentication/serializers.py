from rest_framework import serializers
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name')
        extra_kwargs = {
            'password': {'write_only': True}
        }
    

    def create(self, validated_data):

        user = User.objects.create_user(validated_data['username'], password = validated_data['password'], first_name=validated_data['first_name'], last_name=validated_data['last_name'])

        return user


class LoginSerializer(serializers.ModelSerializer):

    username = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['username', 'password']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']