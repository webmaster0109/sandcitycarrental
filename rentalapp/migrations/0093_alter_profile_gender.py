# Generated by Django 5.0.3 on 2024-03-22 06:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rentalapp", "0092_alter_profile_wishlists"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="gender",
            field=models.CharField(
                blank=True,
                choices=[("Male", "Male"), ("Female", "Female"), ("Others", "Others")],
                max_length=50,
                null=True,
            ),
        ),
    ]