from django.db import models
# from ckeditor.fields import RichTextField
from django_ckeditor_5.fields import CKEditor5Field
from django.contrib.auth.models import User
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation

from django.urls import reverse

# Create your models here.

class BlogsDetail(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    keywords = models.TextField()
    desc = models.TextField()
    blog_image = models.ImageField(upload_to="blogs/image/", null=True, blank=True)
    body = CKEditor5Field(config_name='extends')
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')
    
    def current_hit_count(self):
        return self.hit_count.hits
    
    def get_absolute_url(self):
        return reverse('blog_details', args=[str(self.slug)])
    
    class Meta(object):
        ordering = ['created_at']
    
    def __str__(self):
        return self.title
    
    