# Generated by Django 5.0.2 on 2024-03-05 09:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rentalapp", "0060_alter_cars_year_alter_profile_wishlists"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cars",
            name="year",
            field=models.PositiveIntegerField(blank=True, default=2904, null=True),
        ),
    ]