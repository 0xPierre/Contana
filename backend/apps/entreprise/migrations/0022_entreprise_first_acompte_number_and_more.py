# Generated by Django 4.2.1 on 2024-02-07 16:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("entreprise", "0021_alter_entreprise_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="entreprise",
            name="first_acompte_number",
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name="entreprise",
            name="first_avoir_number",
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name="entreprise",
            name="first_devis_number",
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name="entreprise",
            name="first_facture_number",
            field=models.IntegerField(default=1),
        ),
    ]
