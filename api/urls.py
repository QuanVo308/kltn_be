from django.urls import path
from rest_framework.routers import SimpleRouter
from . import views
from .views import *

route = SimpleRouter()
route.register(r'product', ProductView)
route.register(r'product_test', ProductTestView)

urlpatterns = [

] + route.urls
