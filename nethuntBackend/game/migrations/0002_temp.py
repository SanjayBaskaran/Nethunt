# Generated by Django 4.1.4 on 2023-02-13 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("game", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Temp",
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
                ("temp", models.FileField(upload_to="images")),
            ],
        ),
    ]
