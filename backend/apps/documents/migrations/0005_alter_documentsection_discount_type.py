# Generated by Django 4.2.1 on 2023-08-22 11:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("documents", "0004_alter_documentsection_discount_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="documentsection",
            name="discount_type",
            field=models.CharField(
                choices=[("percentage", "Pourcentage"), ("amount", "Montant")],
                null=True,
            ),
        ),
    ]