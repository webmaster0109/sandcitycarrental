from django.urls import path
from rentalapp.views.admin_dashboard import *
from rentalapp.views.home import *
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
    path('write-review/<slug>', car_review_by_user, name="car_review_by_user"),
    path('like-car-post/<id>', car_like_by_user, name="car_like_by_user"),
    path('add-to-wishlist/<slug>', add_to_wishlists, name="add_to_wishlists"),
    path('delete-reviews/<id>', delete_reviews, name="delete_reviews"),
    path('remove-to-wishlist/<slug>', remove_to_wishlists, name="remove_to_wishlists"),
    path('booking-confirm', success_payment, name="success_payment"),
    
    # authentication urls
    path('auth/login', login_attempt, name="login"),
    path('auth/register', signup_attempt, name="register"),
    path('auth/forgot-password', forgot_password, name="forgot_password"),
    path('dashboard', admin_dashboard_home, name="dashboard"),
    path('dashboard/car-lists', admin_cars_lists, name="car_lists"),
    path('dashboard/notifications', read_notification, name="notification"),
    path('dashboard/user-lists', user_lists, name="user_lists"),
    path('dashboard/wishlists', user_all_wishlists, name="user_all_wishlists"),
    path('dashboard/booking-lists', user_all_bookings, name="user_all_bookings"),
    path('auth/logout', signout, name="logout"),
    path('auth/verify-account/<token>', verify_account, name="verify_account"),
    path('auth/forgot-username', forgot_username, name="forgot_username"),
    path('auth/change-password/<token>', change_password, name="change_password"),
    path('delete-notification/<notification_id>', delete_notification_view, name="delete_notification_view"),

    # user-profile urls
    path('update-details/<user_id>', update_profile, name="update_profile"),
    path('upload-image/<user_id>', upload_image, name="upload_image"),
    path('remove-image/<user_id>', remove_image, name="remove_image"),
    path('delete-user/<user_id>/', delete_user, name="delete_user"),

    # custom page
    path('<str:slug>', custom_page, name="custom_page"),

]
