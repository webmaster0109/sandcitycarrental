from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.conf import settings

class LeadsTasks(models.Model):
    TASKS_STATUS = (
        ('Overdue', 'Overdue'),
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    )
    LEAD_STAGES = (
        ('Basic Discussion', 'Basic Discussion'),
        ('Interested', 'Interested'),
        ('Not Interested', 'Not Interested'),
        ('Rented Car', 'Rented Car'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=TASKS_STATUS, null=True, blank=True)
    task_title = models.CharField(max_length=255, default="Add Task Title")
    task_message = models.TextField(default="Add task")
    lead_stage = models.CharField(max_length=100, choices=LEAD_STAGES)
    date_time = models.DateTimeField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    @property
    def status(self):
        if self.is_completed:
            return 'Completed'
        elif self.date_time is not None:
            current_time = timezone.now()
            overdues_time = self.date_time + timezone.timedelta(days=1)
            if self.date_time > current_time:
                return 'Pending'
            elif current_time > overdues_time:
                return 'Overdue'
            else:
                return 'In Progress'
        else:
            return None

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class LeadsNotes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notes = models.TextField(default="")
    created_on = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class SendMail(models.Model):
    sender = models.CharField(max_length=100, default=settings.EMAIL_HOST_USER)
    receiver = models.ManyToManyField(User, related_name="receivers")
    subject = models.CharField(max_length=255)
    message = CKEditor5Field(config_name='extends', null=True, blank=True)

    def __str__(self):
        return self.subject
    
def send_mail_to_user(sender, receiver, subject, message):
    subject = str(subject)
    html_content = f"""{message}"""
    html_message = strip_tags(html_content)
    message = f"{html_message}\n\n{html_content}"
    admin_email = sender
    user_email = receiver

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=admin_email,
            recipient_list=[user_email],
            html_message=html_content 
        )
    except Exception as e:
        print(f"Failed to send registration email to {admin_email}. Error: {e}")


admin.site.register(SendMail)

@admin.register(LeadsTasks)
class LeadsTasksAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'status']

@admin.register(LeadsNotes)
class LeadsNotesAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'notes']