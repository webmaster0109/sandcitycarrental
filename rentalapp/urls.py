from django.urls import path
from rentalapp.views.admin_dashboard import admin_dashboard_home, admin_cars_lists, signout, update_profile, upload_image, remove_image, user_lists, delete_user, read_notification, delete_notification_view
from rentalapp.views.home import home_page, contact_us, faqs, all_cars, about_us, help_center, car_category, booking_search, car_details, cart, add_to_cart, blogs_page, signup_newsletter, terms_condititon, privacy_policy, PostDetailView
from rentalapp.views.credentials import login_attempt, signup_attempt, forgot_password, verify_account, forgot_username, change_password

urlpatterns = [
    path('', home_page, name="homepage"),
    path('about-us', about_us, name="about_us"),
    path('contact-us', contact_us, name="contact_us"),
    path('faqs', faqs, name="faqs"),
    path('help-center', help_center, name="help_center"),
    path('privacy-policy', privacy_policy, name="privacy_policy"),
    path('terms-conditions', terms_condititon, name="terms_condititon"),
    path('newsletter-signup', signup_newsletter, name="signup_newsletter"),
    path('category/<slug>', car_category, name="car_category"),
    path('search-cars', booking_search, name='booking_search'),
    path('car-detail/<slug>', car_details, name="car_details"),
    path('add-to-cart/<slug>', add_to_cart, name="add_to_cart"),
    path('cart', cart, name="cart"),
    path('blogs', blogs_page, name="blogs_page"),
    path('blog/<str:slug>', PostDetailView.as_view(), name="blog_detail"),
    path('our-cars', all_cars, name="all_cars"),

    # authentication urls
    path('auth/login', login_attempt, name="login"),
    path('auth/register', signup_attempt, name="register"),
    path('auth/forgot-password', forgot_password, name="forgot_password"),
    path('dashboard', admin_dashboard_home, name="dashboard"),
    path('dashboard/car-lists', admin_cars_lists, name="car_lists"),
    path('dashboard/notifications', read_notification, name="notification"),
    path('dashboard/user-lists', user_lists, name="user_lists"),
    path('logout', signout, name="logout"),
    path('verify-account/<token>', verify_account, name="verify_account"),
    path('forgot-username', forgot_username, name="forgot_username"),
    path('change-password/<token>', change_password, name="change_password"),
    path('delete-notification/<notification_id>', delete_notification_view, name="delete_notification_view"),

    # user-profile urls
    path('update-details/<user_id>', update_profile, name="update_profile"),
    path('upload-image/<user_id>', upload_image, name="upload_image"),
    path('remove-image/<user_id>', remove_image, name="remove_image"),
    path('delete-user/<user_id>/', delete_user, name="delete_user"),
]
