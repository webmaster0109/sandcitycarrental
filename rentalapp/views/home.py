from django.shortcuts import render, redirect

def home_page(request):

    return render(request, template_name="frontend/index.html")