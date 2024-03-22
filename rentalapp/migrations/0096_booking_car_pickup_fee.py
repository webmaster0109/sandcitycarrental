# Generated by Django 5.0.3 on 2024-03-22 12:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rentalapp", "0095_booking_company_address_booking_company_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="booking",
            name="car_pickup_fee",
            field=models.PositiveIntegerField(
                blank=True,
                choices=[(0, 0), (100, 100), (200, 200)],
                default=0,
                null=True,
            ),
        ),
    ]
