# Generated by Django 5.0.3 on 2024-03-16 06:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rentalapp", "0088_alter_blogsdetail_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blogsdetail",
            name="slug",
            field=models.SlugField(blank=True, max_length=255, null=True),
        ),
    ]
