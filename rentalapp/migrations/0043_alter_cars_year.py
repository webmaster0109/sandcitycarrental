# Generated by Django 5.0.2 on 2024-02-29 05:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "rentalapp",
            "0042_booking_total_price_booking_user_cars_is_available_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="cars",
            name="year",
            field=models.PositiveIntegerField(blank=True, default=2729, null=True),
        ),
    ]