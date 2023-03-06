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
        # Product.objects.all()
        # p = Product.objects.filter(id = 324)[0]
        # craw_lazada_image(p)

        ps = []
        for p in Product.objects.all():
            if len(p.images.all()) == 0:
                print(p.id)
        #         ps.append(p)
        # craw_lazada_image_multithread(ps)

        return Response('test')

    @action(detail=False, methods=['delete'])
    def delete_all_prodcut(self, request):
        Product.objects.all().delete()
        return Response('delete all product')

    @action(detail=False, methods=['get', 'post'])
    def get_similar_image(self, request):
        product_anchor = ProductTest.objects.filter(
            name=request.GET['name'])[0]
        print(product_anchor)
        all_distance = []
        products = ProductTest.objects.all()
        for product in products:
            print(f'calculating {product.name}')
            if product == product_anchor:
                continue

            anchor_embedding = np.array(product_anchor.embedding_vector)
            test_embedding = np.array(product.embedding_vector)

            # if anchor_embedding.shape != (1,MODEL_OUTPUT_LENGTH) or test_embedding.shape != (1,MODEL_OUTPUT_LENGTH):
            #     return Response(product.name)

            anchor_embedding = normalize(anchor_embedding, axis=1)
            test_embedding = normalize(test_embedding, axis=1)
            distance = cosine_similarity(anchor_embedding, test_embedding)
            all_distance.append(
                {'name': product.name, 'distance': distance[0][0]})

        all_distance = sorted(
            all_distance, key=lambda d: d['distance'], reverse=True)
        name_order = []
        for i in all_distance:
            print(i['name'])
            name_order.append(i['name'])
        return Response({"order_list": name_order, "detail": all_distance})

    @action(detail=False, methods=['get', 'post'])
    def add_data_test(self, request):
        base_dir = pathlib.Path("D:/Downloads/custom_test_dataset/")

        for path in base_dir.glob("*"):
            print(str(path))
            print(path.stem)
            p = ProductTest.objects.filter(image_path=str(path))
            p = ProductTest() if len(p) == 0 else p[0]
            p.name = path.stem
            p.image_path = str(path)
            p.save()
        return Response('ok')

    @action(detail=False, methods=['get'])
    def image_exaction(self, request):

        # response = requests.get("https://cdn.britannica.com/45/5645-050-B9EC0205/head-treasure-flower-disk-flowers-inflorescence-ray.jpg")
        # t = PIL.Image.open(BytesIO(response.content))

        print('loading model')
        m = load_models()

        products = ProductTest.objects.all()
        for product in products:
            print(f'calculating image {product.name}')
            image = PIL.Image.open(pathlib.Path(product.image_path))
            image = image.resize(size=(200, 245))
            image_arr = np.asarray(image)/255.
            embedding_vector = m.predict(np.stack([image_arr]), verbose=0)
            product.embedding_vector = embedding_vector.tolist()
            product.save()

        return Response("ok")

    @action(detail=False, methods=['get'])
    def image_exaction_update(self, request):

        # response = requests.get("https://cdn.britannica.com/45/5645-050-B9EC0205/head-treasure-flower-disk-flowers-inflorescence-ray.jpg")
        # t = PIL.Image.open(BytesIO(response.content))

        print('loading model')
        m = load_models()

        products = ProductTest.objects.all()
        for product in products:
            if len(product.embedding_vector) == 1:
                continue
            print(f'calculating image {product.name}')
            image = PIL.Image.open(pathlib.Path(product.image_path))
            image = image.resize(size=(200, 245))
            image_arr = np.asarray(image)/255.
            embedding_vector = m.predict(np.stack([image_arr]), verbose=0)
            product.embedding_vector = embedding_vector.tolist()
            product.save()

        return Response("ok")

    @action(detail=False, methods=['get'], url_path="crawl_all")
    def crawl_all_data(self, request):
        craw_lazada_all()

        return Response("crawl data done")
