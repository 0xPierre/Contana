# Generated by Django 4.2.1 on 2023-08-07 14:09

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("clients", "0004_clientfiles"),
    ]

    operations = [
        migrations.RenameField(
            model_name="client",
            old_name="siret",
            new_name="siren",
        ),
    ]
