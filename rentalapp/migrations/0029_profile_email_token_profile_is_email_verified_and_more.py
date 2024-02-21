# Generated by Django 5.0.2 on 2024-02-21 10:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rentalapp", "0028_alter_cars_year_alter_profile_dob"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="email_token",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="is_email_verified",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="cars",
            name="year",
            field=models.PositiveIntegerField(blank=True, default=2524, null=True),
        ),
    ]
