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
        print(unquote(request.data['link']).split('?')[0])
        products = Product.objects.filter(link = unquote(request.data['link']).split('?')[0])
        # sources = sources.filter(platform='Shopee', crawled=False)
        
        print(len(products))
        print(products[0])
        return Response('test')

    @action(detail=False, methods=['get', 'post'])
    def test_product_exist(self, request):
        print(unquote(request.data['link']).split('?')[0])
        print(unidecode(request.data['name']))
        # products = Product.objects.filter(link = unquote(request.data['link']).split('?')[0])
        products = Product.objects.filter(name__icontains = unidecode(request.data['name']))
        # sources = sources.filter(platform='Shopee', crawled=False)
        
        print(len(products))
        print(products[0])
        return Response('test')

    @action(detail=False, methods=['delete'])
    def delete_all_prodcut(self, request):
        delete_all_product_multithread()
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
    def add_data_source(self, request):
        request.data._mutable = True
        # request.data["key_words"] = json.loads(request.data["key_words"])
        serializer = SourceDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('ok')

    @action(detail=False, methods=['get'])
    def image_exaction(self, request):

        # response = requests.get("https://cdn.britannica.com/45/5645-050-B9EC0205/head-treasure-flower-disk-flowers-inflorescence-ray.jpg")
        # t = PIL.Image.open(BytesIO(response.content))

        print('loading model')
        m = load_models()
        list_err = []
        images = Image.objects.all()
        for image_instance in images:
            try:
                # print(f'calculating image {image_instance.product.name}')
                response = requests.get(image_instance.link)
                # print(f'dowlonaded image {image_instance.product.name}')
                image = PIL.Image.open(BytesIO(response.content))
                image = image.convert('RGB')
                image = image.resize(size=(200, 245))
                image_arr = np.asarray(image)/255.
                embedding_vector = m.predict(np.stack([image_arr]), verbose=0)
                image_instance.embedding_vector = embedding_vector.tolist()
                image_instance.save()
                # print('\n')
            except Exception as e:
                list_err.append(image_instance.id)
                print(f'{image_instance.id}')
                print(e)

        return Response(list_err)

    @action(detail=False, methods=['get'])
    def image_exaction_update(self, request):

        print('loading model')
        m = load_models()
        list_err = []
        images = Image.objects.all()
        for image_instance in images:
            try:
                if len(image_instance.embedding_vector) == 1:
                    continue
            except:
                pass
            try:

                response = requests.get(image_instance.link)
                # print(f'dowlonaded image {image_instance.product.name}')
                image = PIL.Image.open(BytesIO(response.content))
                image = image.convert('RGB')
                image = image.resize(size=(200, 245))
                image_arr = np.asarray(image)/255.
                embedding_vector = m.predict(np.stack([image_arr]), verbose=0)
                image_instance.embedding_vector = embedding_vector.tolist()
                image_instance.save()
                # print('\n')
            except Exception as e:
                list_err.append(image_instance.id)
                print(f'{image_instance.id}')
                print(e)

        with open("example2.txt", "w", encoding="utf-8") as f:
            for i in list_err:
                f.writelines(f"{i} \n")

        return Response(list_err)

    @action(detail=False, methods=['get'], url_path="crawl_all")
    def crawl_all_data(self, request):
        start = timezone.now()
        # craw_lazada_all()
        delete_all_product_multithread()
        crawl_shopee_categories()
        crawl_shopee_all()
        end = timezone.now()
        print(end - start)
        return Response(end - start)

    @action(detail=False, methods=['get'])
    def crawl_data_source(self, request):
        start = timezone.now()
        # crawl_lazada_categories()
        crawl_shopee_categories()
        end = timezone.now()
        print(end - start)
        return Response(end - start)

    @action(detail=False, methods=['get'])
    def update_fail_pruduct(self, request):
        products = products_have_no_image
        crawl_lazada_image_multithread(products)
        return Response("updated product have no image")


class ProductTestView(viewsets.GenericViewSet,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      #   mixins.DestroyModelMixin,
                      mixins.ListModelMixin):
    queryset = ProductTest.objects.all()
    serializer_class = ProductTestSerializer
    pagination_class = None

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

    @action(detail=False, methods=['get', 'post'])
    def add_data_test(self, request):
        base_dir = pathlib.Path(os.environ.get('TEST_DATASET'))

        for path in base_dir.glob("*"):
            print(str(path))
            print(path.stem)
            p = ProductTest.objects.filter(image_path=str(path))
            p = ProductTest() if len(p) == 0 else p[0]
            p.name = path.stem
            p.image_path = str(path)
            p.save()
        return Response('ok')

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

            euclidean_distance = tf.math.reduce_euclidean_norm(anchor_embedding - test_embedding, axis=1).numpy()
            anchor_embedding = normalize(anchor_embedding, axis=1)
            test_embedding = normalize(test_embedding, axis=1)
            cosine_distance = cosine_similarity(anchor_embedding, test_embedding)
            all_distance.append(
                {'name': product.name, 'cosine_distance': cosine_distance[0][0], 'euclidean_distance': euclidean_distance})

        all_distance = sorted(
            all_distance, key=lambda d: d['cosine_distance'], reverse=True)
        name_order = []
        for i in all_distance:
            print(i['name'])
            name_order.append(i['name'])
        return Response({"order_list": name_order, "detail": all_distance})
