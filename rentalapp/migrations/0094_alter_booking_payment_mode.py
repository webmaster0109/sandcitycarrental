# Generated by Django 5.0.3 on 2024-03-22 07:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rentalapp", "0093_alter_profile_gender"),
    ]

    operations = [
        migrations.AlterField(
            model_name="booking",
            name="payment_mode",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Cash in Hand", "Cash in Hand"),
                    ("Transfer to Bank", "Transfer to Bank"),
                ],
                max_length=50,
                null=True,
            ),
        ),
    ]