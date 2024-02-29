from django.urls import reverse, path
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from rentalapp.models.cars import Cars
import requests
from rentalapp.models.users import Country, Profile, UserNotification
from django.utils import timezone

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
        'country': country,
    }
    return render(request, template_name="backend/dashboard/profile.html", context=context)

@login_required(login_url='/auth/login')
def delete_notification_view(request, notification_id):
    notification = get_object_or_404(UserNotification, id=notification_id)

    # Ensure that the notification belongs to the logged-in user
    if notification.user == request.user:
        notification.delete_notification()
    
    messages.success(request, 'Successfully removed notification')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def unread_notification_count(request):
    total_unread_count = 0
    if request.user.is_authenticated:
        unread_notifications = request.user.usernotification_set.filter(is_read=False)
        total_unread_count = unread_notifications.count()
    return {'total_unread_notifications': total_unread_count}

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
    profile_obj = Profile.objects.get(user=request.user)
    profile_obj.online_status = False
    profile_obj.total_active_time = timezone.now() - profile_obj.last_activity_time
    profile_obj.last_activity_time = timezone.now()
    profile_obj.save()
    logout(request)
    return redirect("dashboard")

@login_required(login_url='/auth/login')
def update_profile(request, user_id):
    if request.method == "POST":
        user_obj = get_object_or_404(User, id=user_id)
        new_first_name = request.POST['first_name']
        new_last_name = request.POST['last_name']
        new_number = request.POST['number']
        new_dob = request.POST['dob']
        new_gender = request.POST['gender']
        try:
            new_country = request.POST['country']
        except KeyError:
            # Handle the case when 'country' key is not present in the POST data
            return HttpResponse("Error: 'country' key not found in the POST data")

        if (
            user_obj.first_name == new_first_name and
            user_obj.last_name == new_last_name and
            user_obj.profile.number == new_number and
            user_obj.profile.dob == new_dob and
            user_obj.profile.gender == new_gender and
            user_obj.profile.country == new_country
        ):
            messages.warning(request, 'No changes were made.')
        else:
            # Update the user and profile details
            user_obj.first_name = new_first_name
            user_obj.last_name = new_last_name
            user_obj.profile.number = new_number
            user_obj.profile.dob = new_dob
            user_obj.profile.gender = new_gender
            user_obj.profile.country = new_country
            user_obj.save()
            user_obj.profile.save()
            messages.success(request, 'Your details have been updated successfully!!!')
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

@login_required(login_url='/authentication/login')
def add_users(request):
    if request.method == "POST":
        pass

@login_required(login_url='/authentication/login')
def read_notification(request):

    notifications = request.user.usernotification_set.all()

    # Mark notifications as read
    for notification in notifications:
        notification.mark_as_read()

    return render(request, template_name="backend/dashboard/notification.html", context={'notifications': notifications})