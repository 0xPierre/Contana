# Generated by Django 4.2.1 on 2025-01-11 07:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("entreprise", "0028_alter_entreprise_options"),
        ("tasks", "0002_task_checked"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="entreprise",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tasks",
                to="entreprise.entreprise",
            ),
            preserve_default=False,
        ),
    ]
