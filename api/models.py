# from djongo import models
from django.db import models
from django.contrib.postgres.fields import ArrayField
# from kltn_be.models import BaseModel
from rest_framework import serializers
# from django.conf import settings

# Create your models here.
class ProductTest(models.Model):
    name = models.CharField(max_length=250, null = True, default={})
    image_url = models.CharField(max_length=250, null= True, default={})
    image_path = models.CharField(max_length=250, null= True, default={})
    embedding_vector = models.TextField(null=True)
    updated_at = models.DateTimeField(auto_now=True,
                                      help_text='Thời gian cập nhật', null=True)
    created_at = models.DateTimeField(auto_now_add=True,
                                      help_text='Thời gian tạo', null=True)

    def __str__(self):
        return self.name
class Category(models.Model):  
    name = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.name}"
    
    def save(self, *args, **kwargs):
        try:
            super(Category, self).save(*args, **kwargs)
        except:
            if not Category.objects.count():
                print('id 1')
                self.id = 1
            else:
                print('id new')
                self.id = Category.objects.last().id + 1
            super(Category, self).save(*args, **kwargs)

class Product(models.Model):
    name = models.TextField(null=True)
    price = models.CharField(max_length=250, null = True, default="")
    link = models.TextField(null=True)
    source_description = models.TextField(null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                related_name='products', null = True)
    crawled = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True,
                                      help_text='Thời gian cập nhật', null=True)
    created_at = models.DateTimeField(auto_now_add=True,
                                      help_text='Thời gian tạo', null=True)

    def __str__(self):
        return self.name

    
    
    # def delete(self, *args, **kwargs):
    #     # print(self.images)
    #     # for image in self.images.all():
    #     #     image.delete()
    #     super(Product, self).delete(self, *args, **kwargs)


class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='images', null = False)
    link = models.TextField(null=True)
    embedding_vector = models.TextField(null=True)
    updated_at = models.DateTimeField(auto_now=True,
                                      help_text='Thời gian cập nhật', null=True)
    created_at = models.DateTimeField(auto_now_add=True,
                                      help_text='Thời gian tạo', null=True)

    
    def __str__(self):
        return f"Image of product {self.product.id}"
    
class SourceData(models.Model):
    platform = models.CharField(max_length=250, null = True, default={})
    link = models.TextField(null=True)
    description = models.TextField(null=True)
    crawled = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True,
                                      help_text='Thời gian cập nhật', null=True)
    created_at = models.DateTimeField(auto_now_add=True,
                                      help_text='Thời gian tạo', null=True)


    def __str__(self):
        return f"{self.platform} {self.link}"
    



