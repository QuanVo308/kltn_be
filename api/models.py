from django.db import models
from kltn_be.models import BaseModel
from rest_framework import serializers

# Create your models here.
class Product(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name