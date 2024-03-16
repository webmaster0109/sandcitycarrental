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
    path('dashboard/pages/my-cars', admin_all_cars, name="admin_all_cars"),
    path('dashboard/pages/car-categories', admin_car_categories, name="admin_car_categories"),
    path('dashboard/pages/new-car', admin_add_new_car, name="admin_add_new_car"),
    path('dashboard/pages/new-feature', admin_new_features, name="admin_new_features"),
    path('dashboard/pages/view-blogs', admin_view_blog, name="admin_view_blog"),

    # add urls
    path('dashboard/pages/add-car-categories', add_car_categories, name="add_car_categories"),
    path('dashboard/pages/add-new-car', add_new_car, name="add_new_car"),
    path('dashboard/pages/add-new-feature', add_new_features, name="add_new_features"),
    path('dashboard/pages/add-new-blog', admin_add_blog, name="admin_add_blog"),

    # get urls
    path('dashboard/pages/show-car/<str:slug>', admin_show_car_details, name="admin_show_car_details"),

    # delete urls
    path('dashboard/apps/delete-booking/<int:id>', delete_booking, name="delete_booking"),
    path('dashboard/apps/delete-customer/<int:user_id>', delete_user, name="delete_user"),
    path('dashboard/pages/delete-car-categories/<str:slug>', admin_delete_category, name="admin_delete_category"),
    path('dashboard/pages/delete-car/<str:slug>', delete_car, name="delete_car"),
    path('dashboard/pages/delete-car-feature/<str:feature_id>', delete_car_features, name="delete_car_features"),

    # update urls
    path('dashboard/pages/update-car-feature/<str:feature_id>', update_car_features, name="update_car_features"),
    path('dashboard/pages/update-car-details/<str:slug>', admin_update_car_details, name="admin_update_car_details"),
    path('dashboard/pages/update-car-category/<str:slug>', update_car_categories, name="update_car_categories"),
]