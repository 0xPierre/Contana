# Generated by Django 4.2.1 on 2023-07-22 23:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("clients", "0002_client_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="client",
            name="archived",
            field=models.BooleanField(default=False),
        ),
    ]