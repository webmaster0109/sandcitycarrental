from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    number = models.CharField(max_length=20, null=True, blank=True)
    profile_image = models.ImageField(upload_to="images/profile/", null=True, blank=True)
    dob = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
    def delete(self, *args, **kwargs):
        if self.profile_image:
            storage, path = self.profile_image.storage, self.profile_image.path
            storage.delete(path)
        super().delete(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        if self.pk:
            try:
                old_instace = Profile.objects.get(pk=self.pk)
                if old_instace.profile_image.name != self.profile_image.name:
                    delete_old_image = old_instace.profile_image.name
                    default_storage.delete(delete_old_image)
            except Profile.DoesNotExist:
                pass
        
        super(Profile, self).save(*args, **kwargs)
