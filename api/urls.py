from django.urls import path
from rest_framework.routers import SimpleRouter
from . import views
from .views import *

route = SimpleRouter()
route.register(r'product', ProductView)

urlpatterns = [

] + route.urls
