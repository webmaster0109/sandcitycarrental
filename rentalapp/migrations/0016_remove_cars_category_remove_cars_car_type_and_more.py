# Generated by Django 5.0.1 on 2024-01-13 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentalapp', '0015_alter_cars_category_alter_cars_year'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cars',
            name='category',
        ),
        migrations.RemoveField(
            model_name='cars',
            name='car_type',
        ),
        migrations.AlterField(
            model_name='cars',
            name='year',
            field=models.PositiveIntegerField(blank=True, default=2814, null=True),
        ),
        migrations.AddField(
            model_name='cars',
            name='car_type',
            field=models.ManyToManyField(to='rentalapp.cartypes'),
        ),
    ]