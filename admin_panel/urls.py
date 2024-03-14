from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard', admin_dashboard, name="admin_dashboard"),
    path('auth/private/login', admin_login, name="admin_login"),
    path('dashboard/apps/calenders', admin_calendar, name="admin_calendar"),
    path('dashboard/apps/customers', admin_customers, name="admin_customers"),
    path('dashboard/apps/notifications', admin_notifications, name="admin_notifications"),
    path('dashboard/apps/orders', admin_user_orders, name="admin_user_orders"),
]