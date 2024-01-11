from django.db import models
import uuid

class CouponCode(models.Model):
    coupon_id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    coupon_code = models.CharField(max_length=100, null=True, blank=True)
    discount_price = models.PositiveIntegerField(default=100, null=True, blank=True)
    minimum_amount = models.PositiveIntegerField(default=100, null=True, blank=True)

    def __str__(self):
        return self.coupon_code
    