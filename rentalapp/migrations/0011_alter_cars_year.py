# Generated by Django 5.0.1 on 2024-01-13 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentalapp', '0010_alter_cars_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cars',
            name='year',
            field=models.PositiveIntegerField(blank=True, default=2306, null=True),
        ),
    ]
