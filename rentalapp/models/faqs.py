from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

class Faq(models.Model):
    question = models.TextField(default="", null=True, blank=True)
    answer = CKEditor5Field(config_name='extends')

    def __str__(self):
        return self.question
    
    # @classmethod
    # def search(self, query):
    #     return self.objects.filter(models.Q(question__icontains=query) | models.Q(answer__icontains=query))