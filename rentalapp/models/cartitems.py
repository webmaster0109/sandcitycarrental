from django.db import models
from django.contrib.auth.models import User
from .cars import Cars
import uuid

class CartItems(models.Model):
    cart_id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart_items", null=True, blank=True)
    cars = models.ForeignKey(Cars, on_delete=models.CASCADE, related_name="cart_items", null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} | {self.cars.brand}"
    