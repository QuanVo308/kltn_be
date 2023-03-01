from djongo import models
from kltn_be.models import BaseModel
from rest_framework import serializers
# from django.conf import settings
# from djongo.storage import GridFSStorage
# grid_fs_storage = GridFSStorage(collection='myfiles', base_url=''.join(["localhost:8000", 'myfiles/']))

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100, null = True)
    image_url = models.CharField(max_length=250, null= True)
    image_path = models.CharField(max_length=100, null= True)
    embedding_vector = models.JSONField(null=True)
    updated_at = models.DateTimeField(auto_now=True,
                                      help_text='Thời gian cập nhật')
    created_at = models.DateTimeField(auto_now_add=True,
                                      help_text='Thời gian tạo')
    # image = models.ImageField(upload_to='testImage', null = True, storage=grid_fs_storage)

    def __str__(self):
        return self.name

    # def delete(self):
    #     t = grid_fs_storage.delete(str(self.image))
    #     super(Product, self).delete()