# Generated by Django 4.1.4 on 2023-01-31 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quiz", "0002_quiz_question"),
    ]

    operations = [
        migrations.AddField(
            model_name="info",
            name="commonMailId",
            field=models.EmailField(max_length=254, null=True),
        ),
    ]
