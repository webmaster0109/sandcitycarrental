from django.db import models
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class EmailNewsletters(models.Model):
    email = models.CharField(max_length=50, null=True, blank=True)
    is_subscribe = models.BooleanField(default=False)

    def __str__(self):
        return self.email or "Email"

user_signature = '\n\nBest regards,\nSandcity Car Rental Pvt. Ltd'

def send_newsletter_email(user_obj):
    subject = f'Congrats {user_obj.email}, You have done Newsletter Signup.'
    # Change the following line to the admin's email address
    recipient_email = f'{user_obj.email}'
    html_message = render_to_string('email/newsletter_email.html', {
        'email': recipient_email, 
    })

    message = strip_tags(html_message)

    admin_subject = f'New Newsletter Signup on Sandcity Car Rental'
    admin_message = f'Email: {user_obj.email}\n\nThank you!\nGo to your admin panel to see complete details of Newsletter.'
    admin_email = settings.EMAIL_HOST_USER 

    try:
        send_mail(subject=subject, message=message, from_email=settings.EMAIL_HOST_USER, recipient_list=[recipient_email], html_message=html_message)
        send_mail(subject=admin_subject, message=admin_message, from_email=settings.EMAIL_HOST_USER, recipient_list=[admin_email])
    except Exception as e:
        print(f"Failed to send registration email to {recipient_email}. Error: {e}")