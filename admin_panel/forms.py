from django import forms
from rentalapp.models.blogs import BlogsDetail



class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogsDetail
        fields = ['body']