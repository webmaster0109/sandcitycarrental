# Generated by Django 5.0.2 on 2024-03-09 11:36

import django_ckeditor_5.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("rentalapp", "0078_faq"),
    ]

    operations = [
        migrations.AlterField(
            model_name="faq",
            name="answer",
            field=django_ckeditor_5.fields.CKEditor5Field(),
        ),
    ]