from djongo import models
# from kltn_be.models import BaseModel
from rest_framework import serializers
# from django.conf import settings
# from djongo.storage import GridFSStorage


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
class Category(models.Model):  
    name = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.name}"
    
    def save(self, *args, **kwargs):
        try:
            super(Category, self).save(*args, **kwargs)
        except:
            if not Category.objects.count():
                # print('id 1')
                self.id = 1
            else:
                # print('id new')
                self.id = Category.objects.last().id + 1
            super(Category, self).save(*args, **kwargs)

class Product(models.Model):
    name = models.CharField(max_length=250, null = True, default="")
    price = models.CharField(max_length=250, null = True, default="")
    link = models.CharField(max_length=250, null = True, default="")
    source_description = models.CharField(max_length=250, null = True, default={})
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                related_name='products', null = True)
    crawled = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True,
                                      help_text='Thời gian cập nhật')
    created_at = models.DateTimeField(auto_now_add=True,
                                      help_text='Thời gian tạo')

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        try:
            super(Product, self).save(*args, **kwargs)
        except:
            if not Product.objects.count():
                # print('id 1')
                self.id = 1
            else:
                # print('id new')
                self.id = Product.objects.last().id + 1
            super(Product, self).save(*args, **kwargs)


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
    
    def save(self, *args, **kwargs):
        try:
            super(Image, self).save(*args, **kwargs)
        except:
            if not Image.objects.count():
                # print('id 1')
                self.id = 1
            else:
                # print('id new')
                self.id = Image.objects.last().id + 1
            super(Image, self).save(*args, **kwargs)
    
class SourceData(models.Model):
    platform = models.CharField(max_length=250, null = True, default={})
    link = models.CharField(max_length=250, null = True, default={})
    description = models.CharField(max_length=250, null = True, default={})
    crawled = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True,
                                      help_text='Thời gian cập nhật')
    created_at = models.DateTimeField(auto_now_add=True,
                                      help_text='Thời gian tạo')


    def __str__(self):
        return f"{self.platform} {self.link}"
    
    def save(self, *args, **kwargs):
        try:
            super(SourceData, self).save(*args, **kwargs)
        except:
            if not SourceData.objects.count():
                # print('id 1')
                self.id = 1
            else:
                # print('id new')
                self.id = SourceData.objects.last().id + 1
            super(SourceData, self).save(*args, **kwargs)
    



