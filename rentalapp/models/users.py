from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    is_email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100, null=True, blank=True)
    number = models.CharField(max_length=20, null=True, blank=True)
    profile_image = models.ImageField(upload_to="images/profile/", null=True, blank=True)
    dob = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True)
    verification_token = models.CharField(max_length=100, null=True, blank=True)
    verification_code = models.CharField(max_length=100, null=True, blank=True)
    is_verified = models.BooleanField(default=False, null=True, blank=True)
    forgot_password_token = models.CharField(max_length=100, null=True, blank=True)

    online_status = models.BooleanField(default=False)
    last_activity_time = models.DateTimeField(null=True, blank=True)
    total_active_time = models.DurationField(default=timezone.timedelta())
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
    def delete(self, *args, **kwargs):
        if self.profile_image:
            storage, path = self.profile_image.storage, self.profile_image.path
            storage.delete(path)
        super().delete(*args, **kwargs)

class Country(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    flag = models.URLField()
    capital = models.CharField(max_length=100, null=True, blank=True)
    languages = models.TextField(default="", null=True, blank=True)
    region = models.CharField(max_length=50, null=True, blank=True)
    subregion = models.CharField(max_length=50, null=True, blank=True)
    maps = models.URLField()
    population = models.CharField(max_length=100, null=True, blank=True)
    timezones = models.CharField(max_length=20, null=True, blank=True)
    currencies = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.name