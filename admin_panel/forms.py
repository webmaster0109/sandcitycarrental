from django import forms
from rentalapp.models.blogs import BlogsDetail
from rentalapp.models.faqs import Faq
from django.utils.text import slugify
from django.utils import timezone
from django.db import models


class BlogForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)
        self.fields['keywords'].initial = 'best car rental services in dubai, car rent in dubai'
        self.fields['desc'].initial = 'Discover the Emirates with our personalized touch, offering you a unique and memorable car rental experience.'
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.slug:
            instance.slug = slugify(instance.title)
        if not instance.created_at:
            instance.created_at = timezone.now()
        if commit:
            instance.save()
        return instance

    class Meta:
        model = BlogsDetail
        fields = ['title', 'keywords', 'desc', 'blog_image', 'body', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Blog Title', 'required': True}),
            'keywords': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Blog Keywords', 'required': True}),
            'desc': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Blog Description', 'required': True}),
            'blog_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class BlogUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BlogUpdateForm, self).__init__(*args, **kwargs)        
        # Check if instance being edited has an image
        if self.instance.pk and self.instance.blog_image:
            self.fields['blog_image'].required = False

    class Meta:
        model = BlogsDetail
        fields = ['title', 'slug', 'keywords', 'desc', 'blog_image', 'body', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Blog Title', 'required': True}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Blog Slug', 'required': True}),
            'keywords': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Blog Keywords', 'required': True}),
            'desc': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Blog Description', 'required': True}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'blog_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class FaqForm(forms.ModelForm):
    class Meta:
        model = Faq
        fields = ['question', 'answer']
        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Question', 'required': True}),
        }

