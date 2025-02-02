# Generated by Django 4.2.10 on 2024-03-21 23:06

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="phone",
            field=models.CharField(
                max_length=25,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Please enter a valid mobile number.",
                        regex="^(\\+\\d{1,3})?\\d{9,13}$",
                    )
                ],
            ),
        ),
    ]
