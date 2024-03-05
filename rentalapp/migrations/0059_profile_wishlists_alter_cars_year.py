# Generated by Django 5.0.2 on 2024-03-04 14:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rentalapp", "0058_carreviews_likes_alter_cars_year"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="wishlists",
            field=models.ManyToManyField(related_name="wishlists", to="rentalapp.cars"),
        ),
        migrations.AlterField(
            model_name="cars",
            name="year",
            field=models.PositiveIntegerField(blank=True, default=2002, null=True),
        ),
    ]
