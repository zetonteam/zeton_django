# Generated by Django 4.2.13 on 2024-08-21 17:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("users", "0005_rename_assignee_point_student"),
    ]

    operations = [
        migrations.AddField(
            model_name="point",
            name="content_type",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="contenttypes.contenttype",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="point",
            name="object_id",
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="point",
            name="points_type",
            field=models.CharField(
                choices=[("task", "task"), ("prize", "prize")],
                default="prize",
                max_length=20,
            ),
        ),
        migrations.AddIndex(
            model_name="point",
            index=models.Index(
                fields=["content_type", "object_id"],
                name="student_poi_content_acfbea_idx",
            ),
        ),
    ]
