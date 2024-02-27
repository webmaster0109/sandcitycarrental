from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

user_signature = '\n\nBest regards,\nSandcity Car Rental Pvt. Ltd'

def send_registration_email(user_obj):
    subject = f'Congrats {user_obj.first_name} {user_obj.last_name}! You have done registration in Sandcity Car Rental.'
    # Change the following line to the admin's email address
    recipient_email = f'{user_obj.email}'
    message = f"Hi {user_obj.email},\n\nYou've successfully registered! Now you can login your account.\n\n\nYour username is {user_obj.username}"

    admin_subject = f'New Registration on Sandcity Car Rental'
    admin_message = f'User Details:\n\nUser Name: {user_obj.first_name} {user_obj.last_name}\nUser Email: {user_obj.email}\n\nThank you!\nSee your admin panel to see complete details of Users.'
    admin_email = settings.EMAIL_HOST_USER 

    try:
        send_mail(subject=subject, message=message, from_email=settings.EMAIL_HOST_USER, recipient_list=[recipient_email])
        send_mail(subject=admin_subject, message=admin_message, from_email=settings.EMAIL_HOST_USER, recipient_list=[admin_email])
    except Exception as e:
        print(f"Failed to send registration email to {recipient_email}. Error: {e}")

def send_forgot_password_mail(request, user_obj, token):
    # forgot password email
    website_url = request.build_absolute_uri('/')[:-1]
    forgot_password_subject = "Your forgot password link"
    forgot_password_message = f"Hi {user_obj.first_name}!\nClick on the link to reset your password {website_url}/change-password/{token}"
    recipient_email = user_obj.email

    try:
        send_mail(subject=forgot_password_subject, message=forgot_password_message, from_email=settings.EMAIL_HOST_USER, recipient_list=[recipient_email])
        return True
    except Exception as e:
        print(f"Failed to send registration email to {recipient_email}. Error: {e}")

def send_verification_mail(request, email, token, otp):
    try:
        website_url = request.build_absolute_uri('/')[:-1]
        forgot_password_subject = "Your registered account needs to be verified."
        forgot_password_message = f"Hi {email}\nYour one time password is {otp}\n\nClick on the link to verify your account {website_url}/verify-account/{token}\n{user_signature}"
        recipient_email = email
        send_mail(subject=forgot_password_subject, message=forgot_password_message, from_email=settings.EMAIL_HOST_USER, recipient_list=[recipient_email])
    except Exception as e:
        print(f"Failed to send registration email to {recipient_email}. Error: {e}")
        return False
    
    return True

def send_forgot_username_mail(request, user_obj):
    try:
        website_url = request.build_absolute_uri('/')[:-1]
        forgot_password_subject = "Your have requested your username."
        forgot_password_message = f"Hi {user_obj.first_name}!\nYour username is {user_obj.username}\nTo login: {website_url}/auth/login\n{user_signature}"
        recipient_email = user_obj.email
        send_mail(subject=forgot_password_subject, message=forgot_password_message, from_email=settings.EMAIL_HOST_USER, recipient_list=[recipient_email])
    except Exception as e:
        print(f"Failed to send registration email to {recipient_email}. Error: {e}")
        return False
    
    return True