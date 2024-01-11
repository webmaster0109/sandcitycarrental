# Generated by Django 5.0.1 on 2024-01-11 10:51

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentalapp', '0004_alter_carfeatures_feature_id_alter_cars_car_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarImages',
            fields=[
                ('car_images_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('car_images', models.ImageField(blank=True, null=True, upload_to='images/cars/')),
            ],
        ),
        migrations.AlterField(
            model_name='carfeatures',
            name='feature_id',
            field=models.CharField(default=90693005, editable=False, max_length=100, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='cars',
            name='car_id',
            field=models.CharField(default=75430874, editable=False, max_length=100, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='cars',
            name='year',
            field=models.PositiveIntegerField(blank=True, default=2581, null=True),
        ),
        migrations.AlterField(
            model_name='cartypes',
            name='types_id',
            field=models.CharField(default=33297749, editable=False, max_length=100, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/profile/'),
        ),
    ]
