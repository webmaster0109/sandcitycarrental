# Generated by Django 5.0.3 on 2024-03-18 05:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("admin_panel", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="LeadsTasks",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Overdue", "Overdue"),
                            ("Pending", "Pending"),
                            ("In Progress", "In Progress"),
                            ("Completed", "Completed"),
                        ],
                        max_length=100,
                    ),
                ),
                ("task_message", models.TextField(default="Add task")),
                (
                    "lead_stage",
                    models.CharField(
                        choices=[
                            ("Interested", "Interested"),
                            ("Not Interested", "Not Interested"),
                            ("Purchased", "Purchased"),
                        ],
                        max_length=100,
                    ),
                ),
                (
                    "lead_source",
                    models.CharField(
                        choices=[
                            ("Inbound Phone Call", "Inbound Phone Call"),
                            ("Direct Traffic", "Direct Traffic"),
                            ("Organic Search", "Organic Search"),
                            ("Social Media", "Social Media"),
                        ],
                        max_length=100,
                    ),
                ),
                ("date_time", models.DateTimeField(blank=True, null=True)),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="CalendarTask",
        ),
    ]
