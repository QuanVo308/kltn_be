from djongo import models
from kltn_be.models import BaseModel
from rest_framework import serializers
# from django.conf import settings
# from djongo.storage import GridFSStorage
# grid_fs_storage = GridFSStorage(collection='myfiles', base_url=''.join(["localhost:8000", 'myfiles/']))

# Create your models here.
class ProductTest(models.Model):
    name = models.CharField(max_length=250, null = True, default={})
    image_url = models.CharField(max_length=250, null= True, default={})
    image_path = models.CharField(max_length=250, null= True, default={})
    embedding_vector = models.JSONField(null=True, default={})
    updated_at = models.DateTimeField(auto_now=True,
                                      help_text='Thời gian cập nhật')
    created_at = models.DateTimeField(auto_now_add=True,
                                      help_text='Thời gian tạo')

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=250, null = True, default="")
    price = models.CharField(max_length=250, null = True, default="")
    link = models.CharField(max_length=250, null = True, default="")
    source_description = models.CharField(max_length=250, null = True, default={})
    updated_at = models.DateTimeField(auto_now=True,
                                      help_text='Thời gian cập nhật')
    created_at = models.DateTimeField(auto_now_add=True,
                                      help_text='Thời gian tạo')

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
    link = models.CharField(max_length=250, null = True, default={})
    embedding_vector = models.JSONField(null=True, default=[])
    updated_at = models.DateTimeField(auto_now=True,
                                      help_text='Thời gian cập nhật')
    created_at = models.DateTimeField(auto_now_add=True,
                                      help_text='Thời gian tạo')

    
    def __str__(self):
        return f"Image of product {self.product.id}"
    
class SourceData(models.Model):
    platform = models.CharField(max_length=250, null = True, default={})
    link = models.CharField(max_length=250, null = True, default={})
    description = models.CharField(max_length=250, null = True, default={})
    crawled = models.BooleanField(default=False)
    # min_page = models.IntegerField(null = True, default=1)
    # max_page = models.IntegerField(null = True)
    # multi_page = models.BooleanField(default=False)
    # key_words = models.JSONField(null=True, default=[])
    updated_at = models.DateTimeField(auto_now=True,
                                      help_text='Thời gian cập nhật')
    created_at = models.DateTimeField(auto_now_add=True,
                                      help_text='Thời gian tạo')


    def __str__(self):
        return f"Image of product {self.product.id}"



