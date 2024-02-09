from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from rentalapp.models.users import Profile, send_registration_email
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login, authenticate

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
        # number = request.POST.get('number')
        # country = request.POST.get('country')
        # profile_image = request.FILES.get('profile_image')

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