from django.db import models
import random
import uuid
import os
from django.core.files.storage import default_storage
from django.contrib.auth.models import User

class CarTypes(models.Model):
    types_id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    car_types = models.CharField(max_length=255, null=True, blank=True)
    category_images = models.ImageField(upload_to="images/category/cars/", null=True, blank=True)
    price_detail = models.TextField(default="", null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)

    def __str__(self):
        return self.car_types

class Cars(models.Model):
    car_id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    car_type = models.ForeignKey(CarTypes, on_delete=models.CASCADE, null=True, blank=True)
    brand = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    year = models.PositiveIntegerField(default=random.randint(2000, 3000), null=True, blank=True)
    desc = models.TextField(default="", null=True, blank=True)

    body_type = models.CharField(max_length=100, null=True, blank=True)
    engine = models.CharField(max_length=255, null=True, blank=True)
    fuel_type = models.CharField(max_length=255, null=True, blank=True)
    exterior_color = models.CharField(max_length=50, null=True, blank=True)

    actual_price = models.PositiveIntegerField(default=100, null=True, blank=True)
    discounted_price = models.PositiveIntegerField(default=50, null=True, blank=True)

    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.brand

class Booking(models.Model):
    car = models.ForeignKey(Cars, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    booking_id = models.CharField(max_length=100, null=True, blank=True)
    pickup_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)
    total_days = models.PositiveIntegerField(default=0, null=True, blank=True)
    total_price = models.PositiveIntegerField(default=0, null=True, blank=True)
    is_paid = models.BooleanField(default=False)

    def total_days(self):
        if self.pickup_date and self.return_date:
            return (self.pickup_date - self.return_date).days
        return None

    def __str__(self):
        return self.car.brand

class CarReviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cars = models.ForeignKey(Cars, on_delete=models.CASCADE, related_name="reviews")
    reviews = models.TextField(default="", null=True, blank=True)
    rating = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} [{self.cars.brand}]"
    


class CarImages(models.Model):
    car_images_id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    cars = models.ForeignKey(Cars, on_delete=models.CASCADE, null=True, blank=True)
    car_images = models.ImageField(upload_to="images/cars/", null=True, blank=True)
    
    def my_instance(self):
        image_name = os.path.basename(self.car_images.name)
        return str(image_name).split('.')[0]

    def __str__(self):
        return f"{self.my_instance()} {self.cars.brand}"
    
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
    