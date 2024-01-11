from django.db import models

class Payment(models.Model):
    payment_id = models.CharField()