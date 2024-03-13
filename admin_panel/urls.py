from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard', admin_dashboard, name="admin_dashboard"),
    path('auth/private/login', admin_login, name="admin_login")
]