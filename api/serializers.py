from rest_framework import serializers
from .models import *
from rest_framework import serializers


class ProductTestSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    image_url = serializers.CharField(required=False)
    image_path = serializers.CharField(required=False)
    embedding_vector = serializers.CharField(required=False)

    class Meta:
        model = ProductTest
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    price = serializers.CharField(required=False)

    class Meta:
        model = ProductTest
        fields = '__all__'
