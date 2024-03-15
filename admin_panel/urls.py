from django.urls import path
from .views import *

urlpatterns = [
    # dashboard urls
    path('dashboard', admin_dashboard, name="admin_dashboard"),
    path('auth/private/login', admin_login, name="admin_login"),

    # app urls
    path('dashboard/apps/calenders', admin_calendar, name="admin_calendar"),
    path('dashboard/apps/customers', admin_customers, name="admin_customers"),
    path('dashboard/apps/notifications', admin_notifications, name="admin_notifications"),
    path('dashboard/apps/bookings', admin_user_orders, name="admin_user_orders"),
    path('dashboard/apps/my-cars', admin_all_cars, name="admin_all_cars"),
    path('dashboard/apps/car-categories', admin_car_categories, name="admin_car_categories"),

    # add urls
    path('dashboard/apps/add-car-categories', add_car_categories, name="add_car_categories"),
    path('dashboard/apps/add-new-car', admin_add_new_car, name="admin_add_new_car"),

    # delete urls
    path('dashboard/apps/delete-booking/<int:id>', delete_booking, name="delete_booking"),
    path('dashboard/apps/delete-customer/<int:user_id>', delete_user, name="delete_user"),
    path('dashboard/apps/delete-car-categories/<str:slug>', admin_delete_category, name="admin_delete_category"),
]