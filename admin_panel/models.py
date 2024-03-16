from django.db import models

# Create your models here.
class CalendarTask(models.Model):
    title = models.CharField(max_length=255)
    start = models.DateTimeField(null=True, blank=True)
    all_day = models.BooleanField(default=True)
    description = models.TextField(default="")
    venue = models.CharField(max_length=100)
    class_name = models.CharField(max_length=100)