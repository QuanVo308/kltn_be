from rest_framework import serializers
from .models import *
from rest_framework import serializers


class SerializerMethodCustomField(serializers.SerializerMethodField):
    def to_representation(self, value):
        try:
            method = getattr(self.parent, self.method_name)
            return method(value)
        except Exception as e:
            print(self.method_name, e)
            return f"<Error {self.method_name}>"


class ProductTestSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    image_url = serializers.CharField(required=False)
    image_path = serializers.CharField(required=False)
    embedding_vector = serializers.CharField(required=False)

    class Meta:
        model = ProductTest
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'link']


class ProductSearchSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    price = serializers.CharField(required=False)
    images = SerializerMethodCustomField(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
        depth = 1

    def get_images(self, obj):
        images = []
        images.append(ImageSerializer(obj.images.all()[0]).data)
        return images


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    price = serializers.CharField(required=False)
    images = SerializerMethodCustomField(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
        depth = 1

    def get_images(self, obj):
        images = []
        for image in obj.images.all():
            images.append(ImageSerializer(image).data)
        return images


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SourceDataSerializer(serializers.ModelSerializer):
    # min_page = serializers.IntegerField(required=False)
    # max_page = serializers.IntegerField(required=False)
    # crawled = serializers.BooleanField(required=False)
    # key_words = serializers.ListField(required=False)

    class Meta:
        model = SourceData
        fields = '__all__'

    # def create(self, validated_data):

    #     # validated_data['key_words'] = validated_data['key_words'][0]
    #     source = SourceData.objects.create(**validated_data)
    #     return source
