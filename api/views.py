from django.shortcuts import render
from .utils import *
from .crawl_shopee import *
from .find_similar import *
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from .serializers import *
from rest_framework.decorators import action
import environ
import os
from django.http import FileResponse
import io
from django.core.files import File
from django.db.models import Count
from .execute import *


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
        base_dir = pathlib.Path('temp')
        for path in base_dir.glob("*"):
            create_time = time.time() - os.path.getctime(path)
            print(path, time.time() - os.path.getctime(path))
            if create_time > 3600:
                try:
                    shutil.rmtree(str(path.resolve()))
                except:
                    pass
                try: 
                    os.remove(str(path.resolve()))
                except:
                    pass

        return Response('test')

    @action(detail=False, methods=['get', 'post'])
    def cleanup_temp(self, request):
        base_dir = pathlib.Path('temp')
        for path in base_dir.glob("*"):
            create_time = time.time() - os.path.getctime(path)
            print(path, time.time() - os.path.getctime(path))
            if create_time > int(request.GET('seconds')):
                try:
                    shutil.rmtree(str(path.resolve()))
                except:
                    pass
                try: 
                    os.remove(str(path.resolve()))
                except:
                    pass

        return Response('cleanup_temp')
    
    @action(detail=False, methods=['get', 'post'])
    def upload_zip(self, request):
        file = request.FILES.get('file', None)
        category_ids = [int(category) for category in request.data['categories'].split(',')]


        file_path = f'temp/{binascii.hexlify(os.urandom(10)).decode("utf8")}_{file.name}'
        folder_path = file_path.split('.')[0]
        
        result = find_similar_from_zip(file, category_ids)

        return Response(result)

    @action(detail=False, methods=['get', 'post'])
    def get_temp_image(self, request):
        img = open(request.GET['path'], 'rb')
        response = FileResponse(img)
        return response

    @action(detail=False, methods=['get', 'post'])
    def re_crawl_category(self, request):
        for _ in range(3):
            products = Product.objects.filter(Q(category__name = 'khac')|Q(category = None))
            print(len(products))
            products = np.array_split(products, len(products)/60)
            
            if len(products) > 0:
                for i in range(len(products)):
                    print(i)
                    crawl_shopee_image_multithread(
                        products[i], recrawl=True, try_time=0)
        
        return Response('re_crawl_category') 

    @action(detail=False, methods=['get', 'post','delete'])
    def delete_product_fail_category(self, request):
        products = Product.objects.filter(Q(category__name = 'khac')|Q(category = None)).delete()
        return   Response('delete_product_fail_category')      

    @action(detail=False, methods=['get', 'post'])
    def count_no_image(self, request):
        product_list = []
        products = Product.objects.annotate(image_count=Count("images")).filter(
            source_description__startswith="Shopee", crawled__in=[True])
        product_list = [
            product for product in products if product.image_count == 0]
        print(len(product_list))
        return Response(len(product_list))

    @action(detail=False, methods=['get', 'post'])
    def test_product_exist(self, request):
        print(unquote(request.data['link']).split('?')[0])
        print(unidecode(request.data['name']))
        query = Q(link__icontains=unquote(request.data['link']).split('?')[0])
        query |= Q(name__icontains=unidecode(request.data['name']))
        # products = Product.objects.filter(link = unquote(request.data['link']).split('?')[0])
        products = Product.objects.filter(query)

        # sources = sources.filter(platform='Shopee', crawled=False)

        print(len(products))
        if len(products) != 0:
            print(products[0])
            return Response(ProductSerializer(products, many=True).data)

        else:
            print("cannot find any product")
        return Response('test')

    @action(detail=False, methods=['delete'])
    def delete_all_product(self, request):
        delete_all_product_multithread()
        return Response('delete all product')

    @action(detail=False, methods=['delete'])
    def delete_all_category(self, request):
        categories = Category.objects.all()
        for category in categories:
            category.delete()
        return Response('delete all category')

    @action(detail=False, methods=['delete'])
    def delete_all_source(self, request):
        SourceData.objects.filter(platform='Shopee').delete()
        return Response('delete all source')

    @action(detail=False, methods=['get', 'post'])
    def find_product(self, request):
        category_ids = request.data.get('categories', [])
        search = request.data.get('name', '')
        # page = request.data.get('page', 1)
        # per_page = request.data.get('per_page', 60)
        print(type(category_ids), category_ids)
        print(type(search), search)

        print(len(search), len(category_ids))
        if len(search) == 0 and len(category_ids) == 0:
            return Response({
                # 'max_page': 10,
                'products': get_random_product_serializer(),
                # 'page': page,
            })

        products = find_product(name=search, category_ids=category_ids)
        # max_page = math.ceil(len(products)/float(per_page))
        # page = max(1, page)
        # page = min(max_page, page)
        # end_indicator = min(len(products), page * per_page)

        # products = products[(page-1) * per_page: end_indicator]

        serializer = ProductSearchSerializer(products, many=True)

        return Response({
            # 'max_page': max_page,
            'products': serializer.data,
            # 'page': page,
        })

    @action(detail=True, methods=['get', 'post'])
    def get_similar_product(self, request, pk):
        # print(request.data['categories'])
        print(request.data['images'])
        anchor_product = self.get_object()
        print(self.get_object())
        images = []
        for image_id in request.data['images']:
            image = Image.objects.filter(id=image_id)[0]
            images.append(image)
        result = get_similar_products_multithread(anchor_product, images)
        print(len(result))
        return Response(result)
        # return Response('result')

    @action(detail=False, methods=['get', 'post'])
    def add_data_source(self, request):
        request.data._mutable = True
        # request.data["key_words"] = json.loads(request.data["key_words"])
        serializer = SourceDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('ok')

    @action(detail=False, methods=['get'])
    def image_exaction_update(self, request):

        update_exact_image_multithread()

        return Response('update image')

    @action(detail=False, methods=['get'])
    def image_exaction_update_rembg(self, request):

        total = 10
        for i in range(total):
            print(f'{i+1}/{total}')
            update_exact_image_multithread_rembg(i, total)

        return Response('update image')

    @action(detail=False, methods=['get'])
    def product_update(self, request):
        product_list = []
        # Product.objects.filter(source_description__startswith="Shopee", crawled__in=[False])
        products = Product.objects.filter(
            source_description__startswith="Shopee", crawled__in=[False])
        if len(products) > 0:
            print(len(products))
            crawl_shopee_image_multithread(products)
        return Response('update product')

    @action(detail=False, methods=['get'])
    def product_recrawl(self, request):
        shopee_recrawl_product()
        return Response('update product')

    @action(detail=False, methods=['get'], url_path="crawl_all")
    def crawl_all_data(self, request):
        start = timezone.now()

        # craw_lazada_all()

        # delete_all_product_multithread()
        # crawl_shopee_categories()
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
    def cleanup_product(self, request):
        cleanup_product()
        return Response("clean up product")


class CategoryView(viewsets.GenericViewSet,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   #   mixins.DestroyModelMixin,
                   mixins.ListModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None

    @action(detail=False, methods=['get', 'post'])
    def test(self, request):
        print(request.data)
        print(request.POST)
        print(type(request.data['categories']))
        return Response('test category')

    @action(detail=False, methods=['get'])
    def get_random(self, request):
        qs = Category.objects.all()
        number = min(len(qs), int(request.GET['quantity']))
        qs = list(qs)
        random.shuffle(qs)
        serializer = CategorySerializer(qs[:number], many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def search(self, request):
        search = unidecode(request.GET['search']).lower()
        search_words = search.split()
        q = Q()
        for word in search_words:
            q &= Q(name__icontains=word)
        qs = Category.objects.filter(q)
        if len(qs) == 0:
            return Response([])

        qs = list(qs)
        number = min(len(qs), int(request.GET['quantity']))
        random.shuffle(qs)
        serializer = CategorySerializer(qs[:number], many=True)

        return Response(serializer.data)


class ProductTestView(viewsets.GenericViewSet,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      #   mixins.DestroyModelMixin,
                      mixins.ListModelMixin):
    queryset = ProductTest.objects.all()
    serializer_class = ProductTestSerializer
    pagination_class = None

    @action(detail=False, methods=['get', 'post'])
    def test(self, request):
        categories = Category.objects.all()
        for category in categories:
            print(f"{category.id}: {len(category.products.all())}")
        return Response('test prododuct')

    @action(detail=True, methods=['get'])
    def get_image(self, request, pk):
        image = ProductTest.objects.filter(id=pk)[0]
        print(image.image_path)
        img = open(image.image_path, 'rb')
        response = FileResponse(img)
        return response

    @action(detail=False, methods=['get'])
    def image_exaction(self, request):

        # response = requests.get("https://cdn.britannica.com/45/5645-050-B9EC0205/head-treasure-flower-disk-flowers-inflorescence-ray.jpg")
        # t = PIL.Image.open(BytesIO(response.content))

        print('loading model')
        # m = load_models()
        session = new_session()

        products = ProductTest.objects.all()
        for product in products:
            print(f'calculating image {product.name}')
            image = PIL.Image.open(pathlib.Path(product.image_path))
            image_rmbg = remove(image, session=session)
            # Create a white rgb background
            new_image = PIL.Image.new("RGB", image_rmbg.size, "WHITE") 
            new_image.paste(image_rmbg, mask = image_rmbg.split()[3])

            image = new_image.resize(size=(200, 245))
            image_arr = np.asarray(image)/255.
            embedding_vector = TRAINNED_MODEL.predict(
                np.stack([image_arr]), verbose=0)
            product.embedding_vector = embedding_vector.tolist()
            product.save()
        

        return Response("ok")

    @action(detail=False, methods=['get'])
    def image_exaction_update(self, request):

        # response = requests.get("https://cdn.britannica.com/45/5645-050-B9EC0205/head-treasure-flower-disk-flowers-inflorescence-ray.jpg")
        # t = PIL.Image.open(BytesIO(response.content))

        print('loading model')
        # m = load_models()

        products = ProductTest.objects.all()
        for product in products:
            if len(product.embedding_vector) == 1:
                continue
            print(f'calculating image {product.name}')
            image = PIL.Image.open(pathlib.Path(product.image_path))
            image = image.resize(size=(200, 245))
            image_arr = np.asarray(image)/255.
            embedding_vector = TRAINNED_MODEL.predict(
                np.stack([image_arr]), verbose=0)
            product.embedding_vector = embedding_vector.tolist()
            product.save()
        

        return Response("ok")

    @action(detail=False, methods=['get', 'post'])
    def add_data_test(self, request):
        ProductTest.objects.all().delete()
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

            anchor_embedding = np.asarray(product_anchor.embedding_vector)
            test_embedding = np.asarray(product.embedding_vector)

            # if anchor_embedding.shape != (1,MODEL_OUTPUT_LENGTH) or test_embedding.shape != (1,MODEL_OUTPUT_LENGTH):
            #     return Response(product.name)
            euclidean_distance = tf.math.reduce_euclidean_norm(
                anchor_embedding - test_embedding, axis=1).numpy()
            anchor_embedding = normalize(anchor_embedding, axis=1)
            test_embedding = normalize(test_embedding, axis=1)
            cosine_distance = cosine_similarity(
                anchor_embedding, test_embedding)
            all_distance.append(
                {'name': product.name, 'id': product.id, 'cosine_distance': cosine_distance[0][0], 'euclidean_distance': euclidean_distance})

        all_distance = sorted(
            all_distance, key=lambda d: d['cosine_distance'], reverse=True)
        name_order = []
        for i in all_distance:
            print(i['name'])
            name_order.append(i['name'])
        return Response({"order_list": name_order, "detail": all_distance})
