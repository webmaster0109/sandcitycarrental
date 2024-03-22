from datetime import datetime
from django import forms
from rentalapp.models.blogs import BlogsDetail
from rentalapp.models.faqs import Faq
from django.utils.text import slugify
from django.utils import timezone
from .models import *
from rentalapp.models.custom_page import CustomPage
from django.contrib.auth.models import User
from rentalapp.models.users import *
from rentalapp.models.cars import *


class UserForm(forms.ModelForm):
    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.username:
            instance.username = str(instance.email).split('@')[0]
        if commit:
            instance.save()
        return instance

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name', 'required': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address', 'required': True}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'required': True}),
        }

class ProfileForm(forms.ModelForm):    
    class Meta:
        model = Profile
        fields = ['user', 'number', 'dob', 'gender', 'country', 'profile_image', 'is_verified']

        widgets = {
            'user': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'gender': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'number': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control', 'required': True}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'required': True}),
            'is_verified': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class BookingForm(forms.ModelForm):
    def save(self, commit=True):
        instance = super().save(commit=False)
        if not isinstance(instance.total_price, int):
            int(instance.total_price)
        if commit:
            instance.save()
        return instance
    class Meta:
        model = Booking
        fields = ['car', 'user', 'booking_id', 'pickup_date', 'return_date', 'total_price', 'payment_mode', 'transaction_id', 'transaction_pdf', 'is_paid']
        widgets = {
            'car': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'user': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'total_price': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'transaction_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Note* Field should be empty if payment mode is "Cash in Hand"'}),
            'transaction_pdf': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'booking_id': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'payment_mode':forms.Select(attrs={'class': 'form-control', 'required': True}),
            'pickup_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'required': True}),
            'return_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'required': True}),
            'is_paid': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


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
            'question': forms.Textarea(attrs={'class': 'form-control', 'required': True, 'rows': 3}),
        }

class LeadsTasksForm(forms.ModelForm):
    class Meta:
        model = LeadsTasks
        fields = ['task_title', 'task_message', 'lead_stage', 'date_time', 'is_completed']
        widgets = {
            'task_title': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'task_message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'required': True}),
            'lead_stage': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control', 'required': True}),
            'is_completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class LeadsNotesForm(forms.ModelForm):
    class Meta:
        model = LeadsNotes
        fields = ['notes', 'is_completed']
        widgets = {
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'required': True}),
            'is_completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class SendMailForm(forms.ModelForm):    
    class Meta:
        model = SendMail
        fields = ['subject', 'message']
        widgets = {
            'subject': forms.TextInput(attrs={'class':'form-control', 'required': True})
        }


class CustomPageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CustomPageForm, self).__init__(*args, **kwargs)
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
        model = CustomPage
        fields = ['title', 'keywords', 'desc', 'page_image', 'body', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Blog Title', 'required': True}),
            'keywords': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Blog Keywords', 'required': True}),
            'desc': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Blog Description', 'required': True}),
            'page_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }