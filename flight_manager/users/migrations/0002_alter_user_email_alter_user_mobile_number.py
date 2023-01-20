# Generated by Django 4.1.5 on 2023-01-20 10:10

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(
                max_length=254, unique=True, verbose_name="email address"
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="mobile_number",
            field=phonenumber_field.modelfields.PhoneNumberField(
                error_messages={
                    "error": "Incorrect International Calling Code or Mobile Number!",
                    "success": False,
                },
                max_length=128,
                region=None,
            ),
        ),
    ]
