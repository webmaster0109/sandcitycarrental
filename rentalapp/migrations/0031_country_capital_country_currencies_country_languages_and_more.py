# Generated by Django 5.0.2 on 2024-02-22 12:53

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rentalapp", "0030_country_alter_cars_year"),
    ]

    operations = [
        migrations.AddField(
            model_name="country",
            name="capital",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="country",
            name="currencies",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name="country",
            name="languages",
            field=models.TextField(blank=True, default="", null=True),
        ),
        migrations.AddField(
            model_name="country",
            name="maps",
            field=models.URLField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="country",
            name="population",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="country",
            name="region",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="country",
            name="subregion",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="country",
            name="timezones",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name="cars",
            name="year",
            field=models.PositiveIntegerField(blank=True, default=2231, null=True),
        ),
    ]
