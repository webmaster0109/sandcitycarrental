# Generated by Django 5.0.3 on 2024-03-16 12:25

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CalendarTask",
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
                ("title", models.CharField(max_length=255)),
                ("start", models.DateTimeField(blank=True, null=True)),
                ("all_day", models.BooleanField(default=True)),
                ("description", models.TextField(default="")),
                ("venue", models.CharField(max_length=100)),
                ("class_name", models.CharField(max_length=100)),
            ],
        ),
    ]
