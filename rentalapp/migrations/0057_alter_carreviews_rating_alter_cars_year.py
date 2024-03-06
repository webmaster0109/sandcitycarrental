# Generated by Django 5.0.2 on 2024-03-04 05:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rentalapp", "0056_alter_carreviews_rating_alter_cars_year"),
    ]

    operations = [
        migrations.AlterField(
            model_name="carreviews",
            name="rating",
            field=models.PositiveIntegerField(
                blank=True,
                choices=[
                    (5, "★★★★★ - 5 Stars"),
                    (4, "★★★★☆ - 4 Stars"),
                    (3, "★★★☆☆ - 3 Stars"),
                    (2, "★★☆☆☆ - 2 Stars"),
                    (1, "★☆☆☆☆ - 1 Stars"),
                ],
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="cars",
            name="year",
            field=models.PositiveIntegerField(blank=True, default=2499, null=True),
        ),
    ]