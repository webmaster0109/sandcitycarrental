from django.db import models
from .cars import Cars
import random

class CarFeatures(models.Model):
    feature_id = models.CharField(max_length=100, primary_key=True, unique=True, editable=False, default=random.randint(10000000, 99999999))
    cars = models.ForeignKey(Cars, on_delete=models.CASCADE, null=True, blank=True)
    features = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.features