# Generated by Django 5.0 on 2023-12-14 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="venue",
            name="email_address",
            field=models.EmailField(
                blank=True, max_length=254, verbose_name="Email Adress"
            ),
        ),
        migrations.AlterField(
            model_name="venue",
            name="phone",
            field=models.CharField(
                blank=True, max_length=25, verbose_name="Contact Phone"
            ),
        ),
        migrations.AlterField(
            model_name="venue",
            name="web",
            field=models.URLField(blank=True, verbose_name="Website Address"),
        ),
    ]
