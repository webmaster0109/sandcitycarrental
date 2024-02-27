from django.urls import path
from rentalapp.views.admin_dashboard import admin_dashboard_home, admin_cars_lists, signout, update_profile, upload_image, remove_image, user_lists, delete_user
from rentalapp.views.home import home_page, contact_us, faqs, about_us
from rentalapp.views.credentials import login_attempt, signup_attempt, forgot_password

urlpatterns = [
    path('', home_page, name="homepage"),
    path('about-us', about_us, name="about_us"),
    path('contact-us', contact_us, name="contact_us"),
    path('faqs', faqs, name="faqs"),

    # authentication urls
    path('auth/login', login_attempt, name="login"),
    path('auth/register', signup_attempt, name="register"),
    path('auth/forgot-password', forgot_password, name="forgot_password"),
    path('dashboard', admin_dashboard_home, name="dashboard"),
    path('dashboard/car-lists', admin_cars_lists, name="car_lists"),
    path('dashboard/user-lists', user_lists, name="user_lists"),
    path('logout', signout, name="logout"),

    path('update-details/<user_id>', update_profile, name="update_profile"),
    path('upload-image/<user_id>', upload_image, name="upload_image"),
    path('remove-image/<user_id>', remove_image, name="remove_image"),
    path('delete-user/<user_id>/', delete_user, name="delete_user"),
]
