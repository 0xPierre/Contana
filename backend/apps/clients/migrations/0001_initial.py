# Generated by Django 4.2.1 on 2023-07-21 18:05

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("entreprise", "0012_rename_num_tva_intracom_entreprise_vat_number"),
    ]

    operations = [
        migrations.CreateModel(
            name="Client",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("socialreasonorname", models.CharField(max_length=255)),
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
                ("phone", models.CharField(blank=True, max_length=255, null=True)),
                ("country", models.CharField(blank=True, max_length=255, null=True)),
                ("city", models.CharField(blank=True, max_length=255, null=True)),
                ("zip_code", models.CharField(blank=True, max_length=255, null=True)),
                ("address", models.CharField(blank=True, max_length=255, null=True)),
                ("vat_number", models.CharField(blank=True, max_length=255, null=True)),
                ("siret", models.CharField(blank=True, max_length=255, null=True)),
                ("note", models.TextField(blank=True, null=True)),
                ("website", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "client_number",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "entreprise",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="clients",
                        to="entreprise.entreprise",
                    ),
                ),
            ],
            options={
                "ordering": ["created_at"],
            },
        ),
    ]