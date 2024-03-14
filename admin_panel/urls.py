from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard', admin_dashboard, name="admin_dashboard"),
    path('auth/private/login', admin_login, name="admin_login"),
    path('dashboard/apps/calenders', admin_calendar, name="admin_calendar"),
    path('dashboard/apps/customers', admin_customers, name="admin_customers"),
    path('dashboard/apps/delete-customer/<int:user_id>', delete_user, name="delete_user"),
    path('dashboard/apps/notifications', admin_notifications, name="admin_notifications"),
    path('dashboard/apps/bookings', admin_user_orders, name="admin_user_orders"),
    path('dashboard/apps/delete-booking/<id>', delete_booking, name="delete_booking")
]