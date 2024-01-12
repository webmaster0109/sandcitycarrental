from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.files.storage import default_storage
from django.utils.text import slugify
from django.utils import timezone

from rentalapp.models.users import Profile
from rentalapp.models.cars import CarImages

@receiver(pre_save, sender=Profile)
def delete_old_image(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = sender.objects.get(pk=instance.pk)
            if old_instance.profile_image.name != instance.profile_image.name:
                default_storage.delete(old_instance.profile_image.path)
        except sender.DoesNotExist:
            pass