from django.db import models
import random
import uuid
import os

class CarTypes(models.Model):
    types_id = models.CharField(max_length=100, primary_key=True, unique=True, editable=False, default=random.randint(10000000, 99999999))
    car_types = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.car_types

class Cars(models.Model):
    car_id = models.CharField(max_length=100, primary_key=True, unique=True, editable=False, default=random.randint(10000000, 99999999))
    car_type = models.ForeignKey(CarTypes, on_delete=models.CASCADE)
    brand = models.CharField(max_length=255, null=True, blank=True)
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
    