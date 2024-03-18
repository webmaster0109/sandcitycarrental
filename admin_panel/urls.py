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
    path('dashboard/apps/contact-forms', admin_contact_form_details, name="admin_contact_form_details"),
    path('dashboard/pages/my-cars', admin_all_cars, name="admin_all_cars"),
    path('dashboard/pages/car-categories', admin_car_categories, name="admin_car_categories"),
    path('dashboard/pages/new-car', admin_add_new_car, name="admin_add_new_car"),
    path('dashboard/pages/new-feature', admin_new_features, name="admin_new_features"),
    path('dashboard/pages/view-blogs', admin_view_blog, name="admin_view_blog"),
    path('dashboard/pages/view-faqs', admin_faqs_list, name="admin_faqs_list"),
    path('dashboard/apps/admin-all-tasks', admin_all_tasks, name="admin_all_tasks"),

    # add urls
    path('dashboard/pages/add-car-categories', add_car_categories, name="add_car_categories"),
    path('dashboard/pages/add-new-car', add_new_car, name="add_new_car"),
    path('dashboard/pages/add-new-feature', add_new_features, name="add_new_features"),
    path('dashboard/pages/add-new-blog', admin_add_blog, name="admin_add_blog"),
    path('dashboard/pages/add-new-faq', admin_new_faqs, name="admin_new_faqs"),
    path('dashboard/apps/add-new-task/<int:id>', admin_add_tasks, name="admin_add_tasks"),
    path('dashboard/apps/add-new-notes/<int:id>', admin_add_notes, name="admin_add_notes"),

    # get urls
    path('dashboard/pages/show-car/<str:slug>', admin_show_car_details, name="admin_show_car_details"),
    path('dashboard/app/show-user-detail/<int:id>', admin_view_user_details, name="admin_view_user_details"),

    # delete urls
    path('dashboard/apps/delete-booking/<int:id>', delete_booking, name="delete_booking"),
    path('dashboard/apps/delete-customer/<int:user_id>', delete_user, name="delete_user"),
    path('dashboard/pages/delete-car-categories/<str:slug>', admin_delete_category, name="admin_delete_category"),
    path('dashboard/pages/delete-car/<str:slug>', delete_car, name="delete_car"),
    path('dashboard/pages/delete-car-feature/<str:feature_id>', delete_car_features, name="delete_car_features"),
    path('dashboard/pages/delete-blog/<str:slug>', admin_delete_blog, name="admin_delete_blog"),
    path('dashboard/pages/delete-faq/<int:id>', admin_delete_faq, name="admin_delete_faq"),
    path('dashboard/apps/delete-contact-form/<int:id>', admin_delete_contact, name="admin_delete_contact"),
    path('dashboard/apps/delete-task/<int:id>', admin_delete_tasks, name="admin_delete_tasks"),
    path('dashboard/apps/delete-notes/<int:id>', admin_delete_notes, name="admin_delete_notes"),

    # update urls
    path('dashboard/pages/update-car-feature/<str:feature_id>', update_car_features, name="update_car_features"),
    path('dashboard/pages/update-car-details/<str:slug>', admin_update_car_details, name="admin_update_car_details"),
    path('dashboard/pages/update-car-category/<str:slug>', update_car_categories, name="update_car_categories"),
    path('dashboard/pages/update-blog/<int:id>', admin_update_blog, name="admin_update_blog"),
    path('dashboard/pages/update-faq/<int:id>', admin_update_faq, name="admin_update_faq"),
    path('dashboard/apps/update-task/<int:id>', admin_edit_tasks, name="admin_edit_tasks"),
]