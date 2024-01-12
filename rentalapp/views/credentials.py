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
        return redirect(reverse('home'))
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username=email)
        if not user_obj.exists():
            messages.warning(request, 'Account not found...')
            return HttpResponseRedirect(request.path_info)
        user_obj = authenticate(username=email, password=password)
        if user_obj:
            login(request, user_obj)
            if 'next' in request.POST:
                return redirect(request.POST['next'])
            return redirect('/')
        messages.warning(request, 'Invalid Credentials!')
        return HttpResponseRedirect(request.path_info)
    return render(request, template_name="backend/credentials/login.html")


def signup_attempt(request):
    if request.user.is_authenticated:
        return redirect(reverse('home'))
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        number = request.POST.get('number')
        password = request.POST.get('password')
        country = request.POST.get('country')
        profile_image = request.FILES.get('profile_image')

        try:
            username = str(email).split('@')[0]
            if User.objects.filter(email=email).first():
                messages.warning(request, 'Email id is already taken.')
            elif User.objects.filter(username=username).first():
                messages.warning(request, 'Username is already taken')
            
            user_obj = User(first_name=first_name, last_name=last_name, email=email, username=username)
            user_obj.set_password(password)
            user_obj.save()
            profile_obj = Profile.objects.create(user=user_obj, number=number, country=country, profile_image=profile_image)
            profile_obj.save()
        except Exception as e:
            print(e)
        
        login(request, user_obj)
        if 'next' in request.POST:
            return redirect(request.POST['next'])
        return redirect('/')
    
    return render(request, template_name="credentials/register.html")