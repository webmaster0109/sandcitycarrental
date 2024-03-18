from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.utils import timezone

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

@admin.register(LeadsTasks)
class LeadsTasksAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'status']

@admin.register(LeadsNotes)
class LeadsNotesAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'notes']