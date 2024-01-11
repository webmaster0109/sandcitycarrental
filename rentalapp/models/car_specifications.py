from django.db import models
from .cars import Cars
import random

class CarSpecifications(models.Model):
    specification_id = models.CharField(max_length=100, primary_key=True, unique=True, editable=False, default=random.randint(10000000, 99999999))
    cars = models.ForeignKey(Cars, on_delete=models.CASCADE, null=True, blank=True)
    body_type = models.CharField(max_length=100, null=True, blank=True)
    engine = models.CharField(max_length=255, null=True, blank=True)
    fuel_type = models.CharField(max_length=255, null=True, blank=True)
    exterior_color = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.cars.brand
    
