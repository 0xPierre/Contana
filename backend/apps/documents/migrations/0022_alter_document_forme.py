# Generated by Django 4.2.1 on 2023-10-22 14:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("documents", "0021_document_file"),
    ]

    operations = [
        migrations.AlterField(
            model_name="document",
            name="forme",
            field=models.CharField(
                choices=[
                    ("facture", "Facture"),
                    ("devis", "Devis"),
                    ("avoir", "Avoir"),
                    ("acompte", "Acompte"),
                ]
            ),
        ),
    ]
