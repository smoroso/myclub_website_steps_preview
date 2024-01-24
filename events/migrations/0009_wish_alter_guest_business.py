# Generated by Django 5.0.1 on 2024-01-22 17:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0008_business_guest_booking"),
    ]

    operations = [
        migrations.CreateModel(
            name="Wish",
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
                ("name", models.CharField(max_length=50)),
                ("email", models.EmailField(max_length=254, null=True)),
                ("phoneNumber", models.CharField(max_length=15, null=True)),
                ("idCard", models.ImageField(null=True, upload_to="")),
                (
                    "regType",
                    models.CharField(
                        choices=[
                            ("Self", "Self"),
                            ("Group", "Group"),
                            ("Corporate", "Corporate"),
                            ("Others", "Others"),
                        ],
                        max_length=25,
                        null=True,
                    ),
                ),
                ("ticketNo", models.IntegerField(default=1)),
            ],
        ),
        migrations.AlterField(
            model_name="guest",
            name="business",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="events.business",
            ),
        ),
    ]