# Generated by Django 5.0.2 on 2024-03-02 08:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rentalapp", "0050_emailnewsletters_alter_cars_year"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cars",
            name="year",
            field=models.PositiveIntegerField(blank=True, default=2355, null=True),
        ),
    ]