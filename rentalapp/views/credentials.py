from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from rentalapp.models.users import Profile
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


def login_attempt(request):
    if request.user.is_authenticated:
        return redirect(reverse('dashboard'))
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username=username)
        if not user_obj.exists():
            messages.warning(request, 'User not found...')
            return redirect('login')
        user_obj = authenticate(username=username, password=password)
        if user_obj:
            login(request, user_obj)
            if 'next' in request.POST:
                return redirect(request.POST['next'])
            return redirect('dashboard')
        messages.warning(request, 'Invalid Credentials!')
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
            if User.objects.filter(email=email).first():
                messages.warning(request, 'Email id is already taken.')
            elif User.objects.filter(username=username).first():
                messages.warning(request, 'Username is already taken')
            
            user_obj = User(first_name=first_name, last_name=last_name, email=email, username=username)
            user_obj.set_password(password)
            user_obj.save()
            profile_obj = Profile.objects.create(user=user_obj)
            profile_obj.save()
        except Exception as e:
            print(e)
        
        login(request, user_obj)
        if 'next' in request.POST:
            return redirect(request.POST['next'])
        return redirect('dashboard')
    
    return render(request, template_name="backend/credentials/register.html")