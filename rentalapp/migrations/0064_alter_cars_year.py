# Generated by Django 5.0.2 on 2024-03-05 10:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rentalapp", "0063_remove_profile_wishlists_alter_cars_year_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cars",
            name="year",
            field=models.PositiveIntegerField(blank=True, default=2293, null=True),
        ),
    ]
