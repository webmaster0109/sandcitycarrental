from django.urls import path
from rentalapp.views.admin_dashboard import admin_dashboard_home, admin_cars_lists, signout, update_profile
from rentalapp.views.home import home_page
from rentalapp.views.credentials import login_attempt, signup_attempt

urlpatterns = [
    path('', home_page, name="homepage"),
    path('auth/login', login_attempt, name="login"),
    path('auth/register', signup_attempt, name="register"),
    path('dashboard', admin_dashboard_home, name="dashboard"),
    path('dashboard/car-lists', admin_cars_lists, name="car_lists"),
    path('logout', signout, name="logout"),

    path('update-details/<user_id>', update_profile, name="update_profile"),
]
