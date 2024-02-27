from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound

def home_page(request):

    return render(request, template_name="frontend/index.html")

def about_us(request):

    return render(request, template_name="frontend/about_us.html")

def contact_us(request):

    return render(request, template_name="frontend/contact_us.html")

def faqs(request):

    return render(request, template_name="frontend/faqs.html")

def handle_unmatched(request, unmatched_path):
    context={
        'unmatched_path': unmatched_path
    }
    return HttpResponseNotFound(HttpResponseNotFound(render(request, template_name='frontend/not_found.html', context=context)))
