# Generated by Django 3.2 on 2024-01-28 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data_producer", "0007_alter_taskresult_task_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="taskresult",
            name="task_id",
            field=models.UUIDField(),
        ),
    ]