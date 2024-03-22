# Generated by Django 5.0.3 on 2024-03-18 05:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("admin_panel", "0002_leadstasks_delete_calendartask"),
    ]

    operations = [
        migrations.AlterField(
            model_name="leadstasks",
            name="status",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Overdue", "Overdue"),
                    ("Pending", "Pending"),
                    ("In Progress", "In Progress"),
                    ("Completed", "Completed"),
                ],
                max_length=100,
                null=True,
            ),
        ),
    ]