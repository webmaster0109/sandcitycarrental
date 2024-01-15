from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound

def home_page(request):

    return render(request, template_name="frontend/index.html")

def handle_unmatched(request, unmatched_path):
    context={
        'unmatched_path': unmatched_path
    }
    return HttpResponseNotFound(HttpResponseNotFound(render(request, template_name='frontend/not_found.html', context=context)))
