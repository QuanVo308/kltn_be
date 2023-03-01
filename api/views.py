from django.shortcuts import render
from .utils import *
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from .serializers import *
from rest_framework.decorators import action
import environ
import os
from django.http import FileResponse
import io
from django.core.files import File
import requests
from io import BytesIO

class ProductView(viewsets.GenericViewSet, 
                  mixins.CreateModelMixin, 
                  mixins.RetrieveModelMixin, 
                  mixins.UpdateModelMixin, 
                #   mixins.DestroyModelMixin,
                  mixins.ListModelMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = None

    @action(detail=False, methods=['get', 'post'])
    def test(self, request):
        products = Product.objects.all()
        for product in products:
            # print(f'calculating image {product.name}')
            # image = PIL.Image.open(pathlib.Path(product.image_path))
            # image = image.resize(size = (200,245))
            # image_arr = np.asarray(image)/255.
            # embedding_vector = m.predict(np.stack([image_arr]), verbose=0)
            # product.embedding_vector = embedding_vector.tolist()
            # product.save()

            print(np.array(product.embedding_vector).shape)
        
        return Response('test')

    @action(detail=False, methods=['get', 'post'])
    def get_similar_image(self, request):
        product_anchor = Product.objects.filter(name = request.GET['name'])[0]
        print(product_anchor)
        all_distance = []
        products = Product.objects.all()
        for product in products:
            print(f'calculating {product.name}')
            if product == product_anchor:
                continue

            anchor_embedding = np.array(product_anchor.embedding_vector)
            test_embedding = np.array(product.embedding_vector)

            if anchor_embedding.shape != (1,128) or test_embedding.shape != (1,128):
                return Response(product.name)
            
            anchor_embedding = normalize(anchor_embedding, axis=1)
            test_embedding = normalize(test_embedding, axis=1)
            distance = cosine_similarity(anchor_embedding, test_embedding)
            all_distance.append({'name': product.name, 'distance': distance[0][0]})

        all_distance = sorted(all_distance, key=lambda d: d['distance'], reverse=True) 
        return Response(all_distance)

    @action(detail=False, methods=['get', 'post'])
    def add_data(self, request):
        
        t = request.data
        product = Product()
        product.image_path = t['image_path']
        product.name = t['name']
        # product.embedding_vector = np.array([[1,2,3,4,5]]).tolist()
        product.save()

        return Response('ok')

    @action(detail=False, methods=['get'])
    def image_exaction(self, request):
        
        # response = requests.get("https://cdn.britannica.com/45/5645-050-B9EC0205/head-treasure-flower-disk-flowers-inflorescence-ray.jpg")
        # t = PIL.Image.open(BytesIO(response.content))

        print('loading model')
        m = keras.models.load_model('D:\QuanVo\KLTN\models\output_kaggle tllds 245x200 out128 float ac66/checkpoint')

        products = Product.objects.all()
        for product in products:
            print(f'calculating image {product.name}')
            image = PIL.Image.open(pathlib.Path(product.image_path))
            image = image.resize(size = (200,245))
            image_arr = np.asarray(image)/255.
            embedding_vector = m.predict(np.stack([image_arr]), verbose=0)
            product.embedding_vector = embedding_vector.tolist()
            product.save()


        return Response("ok")

