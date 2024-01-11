from django.db import models
from django.contrib.auth.models import User
import uuid
from .coupon import CouponCode

class Payment(models.Model):
    payment_id = models.UUIDField(primary_key=True, editable=True, unique=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")
    coupon = models.ForeignKey(CouponCode, on_delete=models.SET_NULL, null=True, blank=True)
    is_paid = models.BooleanField(default=False)

    order_id = models.CharField(max_length=255, null=True, blank=True)
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username | self.order_id}"
    