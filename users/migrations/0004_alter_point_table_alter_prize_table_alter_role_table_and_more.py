# Generated by Django 4.2.9 on 2024-01-10 18:40

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_alter_caregiver_id_alter_customuser_id_and_more"),
    ]

    operations = [
        migrations.AlterModelTable(
            name="point",
            table="student_points",
        ),
        migrations.AlterModelTable(
            name="prize",
            table="student_prizes",
        ),
        migrations.AlterModelTable(
            name="role",
            table="roles",
        ),
        migrations.AlterModelTable(
            name="student",
            table="students",
        ),
        migrations.AlterModelTable(
            name="task",
            table="student_tasks",
        ),
    ]
