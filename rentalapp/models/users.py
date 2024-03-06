from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .cars import Cars

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    number = models.CharField(max_length=20, null=True, blank=True)
    profile_image = models.ImageField(upload_to="images/profile/", null=True, blank=True)
    dob = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    verification_token = models.CharField(max_length=100, null=True, blank=True)
    verification_code = models.CharField(max_length=100, null=True, blank=True)
    is_verified = models.BooleanField(default=False, null=True, blank=True)
    forgot_password_token = models.CharField(max_length=100, null=True, blank=True)

    online_status = models.BooleanField(default=False)
    last_activity_time = models.DateTimeField(null=True, blank=True)
    total_active_time = models.DurationField(default=timezone.timedelta())
    wishlists = models.ManyToManyField(Cars, related_name="wishlists")

    def get_total_wishlists(self):
        return self.wishlists.count()
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
    def delete(self, *args, **kwargs):
        if self.profile_image:
            storage, path = self.profile_image.storage, self.profile_image.path
            storage.delete(path)
        super().delete(*args, **kwargs)

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

class Country(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    flag = models.URLField()
    capital = models.CharField(max_length=100, null=True, blank=True)
    languages = models.TextField(default="", null=True, blank=True)
    region = models.CharField(max_length=50, null=True, blank=True)
    subregion = models.CharField(max_length=50, null=True, blank=True)
    maps = models.URLField()
    population = models.CharField(max_length=100, null=True, blank=True)
    timezones = models.CharField(max_length=20, null=True, blank=True)
    currencies = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.name
    
class ContactUs(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    number = models.CharField(max_length=20, null=True, blank=True)
    message = models.TextField(default="", null=True, blank=True)

    def __str__(self):
        return self.name

def send_contact_form_email(user_obj):

    admin_subject = f'Get New Contact Form on Sandcity Car Rental'
    admin_message = f'Contact Form Details:\nName: {user_obj.name}\nEmail: {user_obj.email}\nPhone: {user_obj.number}\nMessage: {user_obj.message}\n\nThank you!\nSee your admin panel to see complete details of Users.'
    admin_email = settings.EMAIL_HOST_USER 

    try:
        send_mail(subject=admin_subject, message=admin_message, from_email=settings.EMAIL_HOST_USER, recipient_list=[admin_email])
    except Exception as e:
        print(f"Failed to send registration email to {admin_email}. Error: {e}")


class UserNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField(default="", null=True, blank=True)
    message = models.TextField(default="", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def mark_as_read(self):
        self.is_read = True
        self.save()
    
    def delete_notification(self):
        self.delete()

    def __str__(self):
        return self.title