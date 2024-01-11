from django.db import models
from .cars import Cars
import uuid

class CarSpecifications(models.Model):
    specification_id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    cars = models.ForeignKey(Cars, on_delete=models.CASCADE)
    body_type = models.CharField(max_length=100, null=True, blank=True)
    engine = models.CharField(max_length=255, null=True, blank=True)
    fuel_type = models.CharField(max_length=255, null=True, blank=True)
    exterior_color = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.cars.brand
    
