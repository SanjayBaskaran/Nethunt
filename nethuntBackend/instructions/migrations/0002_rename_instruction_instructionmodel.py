# Generated by Django 4.1.4 on 2022-12-27 16:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("instructions", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Instruction",
            new_name="InstructionModel",
        ),
    ]
