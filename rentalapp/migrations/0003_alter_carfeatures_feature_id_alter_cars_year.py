# Generated by Django 5.0.1 on 2024-01-11 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentalapp', '0002_alter_carfeatures_feature_id_alter_cars_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carfeatures',
            name='feature_id',
            field=models.CharField(default=15205732, editable=False, max_length=100, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='cars',
            name='year',
            field=models.PositiveIntegerField(blank=True, default=2627, null=True),
        ),
    ]