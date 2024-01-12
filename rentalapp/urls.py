from django.urls import path
from rentalapp.views.admin_dashboard import admin_dashboard_home
from rentalapp.views.home import home_page
from rentalapp.views.credentials import login_attempt

urlpatterns = [
    path('', home_page, name="homepage"),
    path('auth/login', login_attempt, name="login"),
    path('dashboard', admin_dashboard_home, name="dashboard")
]
