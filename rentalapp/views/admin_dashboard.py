from django.urls import reverse, path
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect


@login_required(login_url='/auth/login')
def admin_dashboard_home(request):
    user = request.user
    print(request.user)
    return render(request, template_name="backend/dashboard/profile.html")