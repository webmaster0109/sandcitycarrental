# Generated by Django 5.0.2 on 2024-02-29 12:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rentalapp", "0044_alter_cars_year"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="booking",
            name="pickup_date",
        ),
        migrations.RemoveField(
            model_name="booking",
            name="return_date",
        ),
        migrations.AddField(
            model_name="booking",
            name="booking_id",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="booking",
            name="is_paid",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="cars",
            name="year",
            field=models.PositiveIntegerField(blank=True, default=2337, null=True),
        ),
    ]
