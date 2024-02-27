from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from rentalapp.models.users import Profile, send_registration_email
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login, authenticate
from rentalapp.helpers import *
import uuid
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from datetime import timedelta, datetime
from django.utils.safestring import mark_safe
import random

def login_attempt(request):
    if request.user.is_authenticated:
        return redirect(reverse('dashboard'))
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = authenticate(request, username=username, password=password)
        if user_obj:
            login(request, user_obj)
            if 'next' in request.POST:
                return redirect(request.POST['next'])
            return redirect('dashboard')
        else:
            messages.warning(request, 'Invalid username or password. Please try again.')
            return redirect('login')
    return render(request, template_name="backend/credentials/login.html")

def signup_attempt(request):
    if request.user.is_authenticated:
        return redirect(reverse('dashboard'))
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match. Please enter matching passwords.")
            return redirect('register')

        try:
            username = str(email).split('@')[0]
            user_obj, created = User.objects.get_or_create(email=email, defaults={'first_name': first_name, 'last_name': last_name, 'username': username})
            user_obj.set_password(password)
            if not created:
                messages.warning(request, 'Email or username is already taken.')
                return redirect('register')
            user_obj.save()
            send_registration_email(user_obj)
            profile_obj = Profile.objects.create(user=user_obj)
            profile_obj.save()
            
        except Exception as e:
            print(e)
        
        login(request, user_obj, backend='django.contrib.auth.backends.ModelBackend')
        if 'next' in request.POST:
            return redirect(request.POST['next'])
        return redirect('dashboard')
    
    return render(request, template_name="backend/credentials/register.html")

def forgot_password(request):
    try:
        if request.method == "POST":
            username = request.POST.get('username')
            user_obj = User.objects.filter(username=username).first()
            if not user_obj:
                messages.warning(request, f"Sorry, There is no username of {username} exists. Register now!")
                return redirect('register')
            
            profile_obj = Profile.objects.get(user=user_obj)

            last_sent_time = profile_obj.modified_at
            if last_sent_time and (timezone.now() - last_sent_time) < timedelta(minutes=10) and profile_obj.forgot_password_token != None:
                time_difference = timezone.now() - last_sent_time
                remaining_time = max(0, 10 - time_difference.total_seconds() / 60)
                if remaining_time > 0:
                    countdown = f'<strong style="font-size:20px;">{int(remaining_time)} minutes</strong>'
                    messages.warning(request, mark_safe(f"Please wait, {countdown} left before requesting another forgot password link."))
                    return redirect('forgot_password')

            token = str(uuid.uuid4())
            profile_obj.forgot_password_token = token
            profile_obj.modified_at = timezone.now()
            profile_obj.save()
            send_forgot_password_mail(request, user_obj, token)
            messages.success(request, f"We've sent you forgot password link on your {user_obj.email}")
            return redirect('forgot_password')

    except Exception as e:
        print(e)
    return render(request, template_name="backend/credentials/forgot_password.html")

def check_password_similarity(new_password, old_password):
    common_characters = set(new_password) & set(old_password)
    similarity_percentage = (len(common_characters) / len(old_password)) * 100
    return similarity_percentage >= 30

def change_password(request, token):
    try:
        profile_obj = Profile.objects.filter(forgot_password_token=token).first()

        if not profile_obj:
            messages.warning(request, "Invalid or expired password reset link. Please request a new one.")
            return redirect('forgot_password')
        
        if profile_obj and profile_obj.modified_at + timedelta(minutes=10) < timezone.now():
            # Token has expired, remove it from the database
            profile_obj.forgot_password_token = None
            profile_obj.save()
            messages.warning(request, "The password reset link has expired. Please request a new one.")
            return redirect('forgot_password')

        if request.method == "POST":
            new_password = request.POST.get("password")
            confirm_new_password = request.POST.get("confirm-password")
            user_id = request.POST.get("user_id")

            if user_id is None:
                messages.warning(request, "Oops! No User ID found.")
                return redirect(f'/change-password/{token}')
            
            if new_password != confirm_new_password:
                messages.warning(request, "Both passwords must be same!")
                return redirect(f'/change-password/{token}')
            
            user_obj = User.objects.get(id=user_id)

            if check_password(new_password, user_obj.password):
                messages.warning(request, "You chose the old password. Please create a new and different one.")
                return redirect(f'/change-password/{token}')
            
            if check_password_similarity(new_password, user_obj.password):
                messages.warning(request, "The new password is too similar to the old password. Please choose a different one.")
                return redirect(f'/change-password/{token}')

            user_obj.set_password(new_password)
            user_obj.save()
            profile_obj.forgot_password_token = None
            profile_obj.modified_at = timezone.now()
            profile_obj.save()
            messages.success(request, "Succesfully password has changed. Login now!")
            return redirect('/auth/login')
    except Exception as e:
        print(e)
    return render(request, template_name="change_password.html", context={'profile': profile_obj.user.id})

def forgot_username(request):
    try:
        if request.method == "POST":
            email = request.POST.get('email')
            user_obj = User.objects.filter(email=email).first()
            if not user_obj:
                messages.warning(request, f"Sorry, There is no {email} exists. Register now!")
                return redirect('register')
            
            profile_obj = Profile.objects.get(user=user_obj)

            last_sent_time = profile_obj.modified_at
            if last_sent_time and (timezone.now() - last_sent_time) < timedelta(minutes=10):
                time_difference = timezone.now() - last_sent_time
                remaining_time = max(0, 10 - time_difference.total_seconds() / 60)
                print(remaining_time)
                if remaining_time > 0:
                    countdown = f'<strong style="font-size:20px;">{int(remaining_time)} minutes</strong>'
                    messages.warning(request, mark_safe(f"We've already sent your username on {email}, wait for {countdown} before requesting username again."))
                    return redirect('forgot_username')

            profile_obj.modified_at = timezone.now()
            profile_obj.save()
            send_forgot_username_mail(request, user_obj)
            messages.success(request, f"We've sent your username on your {user_obj.email}")
            return redirect('forgot_username')

    except Exception as e:
        print(e)
    return render(request, template_name="forgot_username.html")