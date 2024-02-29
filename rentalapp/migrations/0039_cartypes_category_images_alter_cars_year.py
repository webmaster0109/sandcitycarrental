# Generated by Django 5.0.2 on 2024-02-28 09:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rentalapp", "0038_remove_cars_category_alter_cars_year"),
    ]

    operations = [
        migrations.AddField(
            model_name="cartypes",
            name="category_images",
            field=models.ImageField(
                blank=True, null=True, upload_to="images/category/cars/"
            ),
        ),
        migrations.AlterField(
            model_name="cars",
            name="year",
            field=models.PositiveIntegerField(blank=True, default=2599, null=True),
        ),
    ]
