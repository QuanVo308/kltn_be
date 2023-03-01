from django.db import models

# class BaseQuerySet(models.QuerySet):
#     def soft_delete(self):
#         return self.update(deleted=True)
    


# class BaseModelManager(models.Manager):
#     def get_queryset(self):
#         return BaseQuerySet(self.model, using=self._db).filter(deleted=False)
    
class BaseModel(models.Model):
    # deleted = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True,
                                      help_text='Thời gian cập nhật')
    created_at = models.DateTimeField(auto_now_add=True,
                                      help_text='Thời gian tạo')
    # objects = BaseModelManager()
    # all_objects = models.Manager()

    def restore(self):
        self.deleted = False
        self.save()

    # def delete(self, *args, **kwargs):
    #     self.deleted = True
    #     self.save()

    class Meta:
        abstract = True