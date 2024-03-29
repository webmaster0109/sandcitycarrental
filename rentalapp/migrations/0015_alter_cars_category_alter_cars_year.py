# Generated by Django 5.0.1 on 2024-01-13 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentalapp', '0014_alter_cars_category_alter_cars_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cars',
            name='category',
            field=models.CharField(choices=[('Premium', 'Premium'), ('Economy', 'Economy'), ('Sports', 'Sports'), ('7Seaters', '7Seaters')], default='Premium', max_length=20),
        ),
        migrations.AlterField(
            model_name='cars',
            name='year',
            field=models.PositiveIntegerField(blank=True, default=2236, null=True),
        ),
    ]
