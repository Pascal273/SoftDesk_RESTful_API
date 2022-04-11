from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer


class UserSerializer(NestedHyperlinkedModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'url']


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'password': {'style': {'input_type': 'password'}}}

    def create(self, validated_data):
        user = get_user_model()
        user.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
