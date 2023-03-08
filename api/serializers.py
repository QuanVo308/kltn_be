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

class SourceDataSerializer(serializers.ModelSerializer):
    min_page = serializers.IntegerField(required=False)
    max_page = serializers.IntegerField(required=False)
    multi_page = serializers.BooleanField(required=False)
    key_words = serializers.ListField(required=False)
    
    class Meta:
        model = SourceData
        fields = '__all__'
    
    def create(self, validated_data):
        
        validated_data['key_words'] = validated_data['key_words'][0]
        source = SourceData.objects.create(**validated_data)
        return source
