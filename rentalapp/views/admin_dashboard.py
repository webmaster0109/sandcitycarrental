from django.urls import reverse, path
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from rentalapp.models.cars import Cars
import datetime

@login_required(login_url='/auth/login')
def admin_dashboard_home(request):
    user = request.user
    return render(request, template_name="backend/dashboard/profile.html")

@login_required(login_url='/auth/login')
def admin_cars_lists(request):
    category_filter = request.GET.get('category', None)
    if category_filter:
        cars = Cars.objects.filter(category=category_filter)
    else:
        cars = Cars.objects.all()
    context = {
        'cars': cars,
        'category_filter': category_filter
    }
    return render(request, template_name="backend/dashboard/car_lists.html", context=context)

def signout(request):
    logout(request)
    return redirect("dashboard")

@login_required(login_url='/auth/login')
def update_profile(request, user_id):
    if request.method == "POST":
        user_obj = get_object_or_404(User, id=user_id)
        user_obj.first_name = request.POST['first_name']
        user_obj.last_name = request.POST['last_name']
        user_obj.profile.number = request.POST['number']
        user_obj.profile.dob = request.POST['dob']
        user_obj.profile.gender = request.POST['gender']
        user_obj.profile.country = request.POST['country']
        user_obj.save()
        user_obj.profile.save()
        messages.success(request, 'Your details has been updated successfully!!!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))