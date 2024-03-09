from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

class CustomPage(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    desc = models.TextField(default="", null=True, blank=True)
    keywords = models.TextField(default="", null=True, blank=True)
    page_image = models.ImageField(upload_to="images/custom_page/", null=True, blank=True)
    body = CKEditor5Field(config_name='extends')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    