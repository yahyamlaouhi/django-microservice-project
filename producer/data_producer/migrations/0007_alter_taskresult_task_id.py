# Generated by Django 3.2 on 2024-01-28 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data_producer", "0006_taskresult"),
    ]

    operations = [
        migrations.AlterField(
            model_name="taskresult",
            name="task_id",
            field=models.UUIDField(editable=False),
        ),
    ]