# Generated by Django 5.0.7 on 2024-07-30 03:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="attendance",
            name="attendance_date",
        ),
        migrations.AlterField(
            model_name="attendance",
            name="status",
            field=models.CharField(
                choices=[
                    ("Present", "Present"),
                    ("Absent", "Absent"),
                    ("Excused", "Excused"),
                ],
                max_length=10,
            ),
        ),
    ]
