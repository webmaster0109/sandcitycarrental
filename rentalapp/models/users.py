from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    number = models.CharField(max_length=20, null=True, blank=True)
    profile_image = models.ImageField(upload_to="images/profile/", null=True, blank=True)
    dob = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return self.user.username
    
    def delete(self, *args, **kwargs):
        if self.profile_image:
            storage, path = self.profile_image.storage, self.profile_image.path
            storage.delete(path)
        super().delete(*args, **kwargs)
