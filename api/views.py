from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from .serializers import *
from rest_framework.decorators import action

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
        print('check')
        return Response('check')

