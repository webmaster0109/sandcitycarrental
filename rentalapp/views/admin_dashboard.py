from django.urls import reverse, path
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from rentalapp.models.cars import Cars
import requests
from rentalapp.models.users import Country, Profile

@login_required(login_url='/auth/login')
def admin_dashboard_home(request):
    user = request.user
    dob = request.user.profile.dob
    date_of_birth = ""
    if dob is not None:
        date_of_birth = dob.strftime("%Y-%m-%d")
    else:
        pass

    country = Country.objects.all()

    context = {
        'date_object' : date_of_birth,
        'country': country
    }
    return render(request, template_name="backend/dashboard/profile.html", context=context)

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
        try:
            user_obj.profile.country = request.POST['country']
        except KeyError:
            # Handle the case when 'country' key is not present in the POST data
            return HttpResponse("Error: 'country' key not found in the POST data")
        user_obj.save()
        user_obj.profile.save()
        messages.success(request, 'Your details has been updated successfully!!!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/authentication/login')
def upload_image(request, user_id):
    if request.method == "POST":
        user_obj = get_object_or_404(User, id=user_id)
        user_obj.profile.profile_image = request.FILES['profile_img']
        user_obj.profile.save()
        messages.success(request, 'Image has been uploaded successfully!!!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/authentication/login')
def remove_image(request, user_id):
    user_obj = User.objects.get(id=user_id)
    
    if user_obj.profile.profile_image:
        user_obj.profile.profile_image = None
        user_obj.profile.save()
        
        messages.success(request, 'Image removed.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    if not user_obj.profile.profile_image:
        messages.warning(request, 'Image is not exists anymore.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/authentication/login')
def user_lists(request):

    user_profile = Profile.objects.all()

    context = {'user_profile': user_profile}

    return render(request, template_name="backend/dashboard/user_lists.html", context=context)

@login_required(login_url='/authentication/login')
def delete_user(request, user_id):    
    if request.method == 'POST':
        users = get_object_or_404(User, id=user_id)
        # Perform the deletion
        users.delete()
        return redirect("user_lists")
