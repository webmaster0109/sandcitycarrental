# Generated by Django 5.0.1 on 2024-01-13 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentalapp', '0025_alter_cars_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cars',
            name='year',
            field=models.PositiveIntegerField(blank=True, default=2230, null=True),
        ),
    ]
