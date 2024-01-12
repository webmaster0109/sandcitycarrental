from django.db import models
import random
import uuid
import os
from django.core.files.storage import default_storage

class CarTypes(models.Model):
    types_id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    car_types = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)

    def __str__(self):
        return self.car_types

class Cars(models.Model):
    car_id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    car_type = models.ForeignKey(CarTypes, on_delete=models.CASCADE)
    brand = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    year = models.PositiveIntegerField(default=random.randint(2000, 3000), null=True, blank=True)
    desc = models.TextField(default="", null=True, blank=True)
    price = models.PositiveIntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.brand

class CarImages(models.Model):
    car_images_id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    cars = models.ForeignKey(Cars, on_delete=models.CASCADE, null=True, blank=True)
    car_images = models.ImageField(upload_to="images/cars/", null=True, blank=True)
    
    def my_instance(self):
        image_name = os.path.basename(self.car_images.name)
        return str(image_name).split('.')[0]

    def __str__(self):
        return self.my_instance()
    
    def delete(self, *args, **kwargs):
        if self.car_images:
            storage, path = self.car_images.storage, self.car_images.path
            storage.delete(path)
        super().delete(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        if self.pk:
            try:
                old_instance = CarImages.objects.get(pk=self.pk)
                if old_instance.car_images.name != self.car_images.name:
                    old_image_path = old_instance.car_images.path
                    default_storage.delete(old_image_path)
            except CarImages.DoesNotExist:
                pass
        super(CarImages, self).save(*args, **kwargs)
    