# Generated by Django 5.0.2 on 2024-02-28 09:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rentalapp", "0039_cartypes_category_images_alter_cars_year"),
    ]

    operations = [
        migrations.AddField(
            model_name="cartypes",
            name="price_detail",
            field=models.TextField(blank=True, default="", null=True),
        ),
        migrations.AlterField(
            model_name="cars",
            name="year",
            field=models.PositiveIntegerField(blank=True, default=2508, null=True),
        ),
    ]
