# Generated by Django 5.0.1 on 2024-01-15 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0006_event_approved"),
    ]

    operations = [
        migrations.CreateModel(
            name="Star",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=50)),
                ("last_name", models.CharField(max_length=50)),
                ("email", models.EmailField(max_length=254)),
                ("phone", models.CharField(max_length=12)),
            ],
        ),
    ]
