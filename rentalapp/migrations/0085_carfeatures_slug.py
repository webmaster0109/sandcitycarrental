# Generated by Django 5.0.3 on 2024-03-15 10:59

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rentalapp", "0084_rename_is_available_cars_in_stock_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="carfeatures",
            name="slug",
            field=models.PositiveIntegerField(
                default=django.utils.timezone.now, editable=False, unique=True
            ),
            preserve_default=False,
        ),
    ]
