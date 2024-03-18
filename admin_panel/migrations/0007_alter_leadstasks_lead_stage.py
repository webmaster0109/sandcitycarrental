# Generated by Django 5.0.3 on 2024-03-18 06:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("admin_panel", "0006_leadstasks_task_title"),
    ]

    operations = [
        migrations.AlterField(
            model_name="leadstasks",
            name="lead_stage",
            field=models.CharField(
                choices=[
                    ("Interested", "Interested"),
                    ("Not Interested", "Not Interested"),
                    ("Rented Car", "Rented Car"),
                ],
                max_length=100,
            ),
        ),
    ]
