from django.shortcuts import render
from .utils import *
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from .serializers import *
from rest_framework.decorators import action
from pymongo import *
client = MongoClient('connection_string')
db = client['db_name']


class ProductView(viewsets.GenericViewSet, 
                  mixins.CreateModelMixin, 
                  mixins.RetrieveModelMixin, 
                  mixins.UpdateModelMixin, 
                  mixins.DestroyModelMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = None

    @action(detail=False, methods=['get'])
    def check(self, request):
        img = PIL.Image.open(pathlib.Path("D:\Picture\ThaoNguyenHoa\IMG_2211.JPG"))
        img_p = PIL.Image.open(pathlib.Path("D:\Picture\ThaoNguyenHoa\IMG_2214.JPG"))
        img_n = PIL.Image.open(pathlib.Path("D:\Picture\ThaoNguyenHoa\IMG_2219.JPG"))

        img = img.resize(size = (200,245))
        img_p = img_p.resize(size = (200,245))
        img_n = img_n.resize(size = (200,245))

        img_arr = np.asarray(img)/255.
        img_p_arr = np.asarray(img_p)/255.
        img_n_arr = np.asarray(img_n)/255.

        return Response({
            "img_arr": img_arr
        })

