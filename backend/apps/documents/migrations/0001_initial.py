# Generated by Django 4.2.1 on 2023-08-21 20:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("entreprise", "0014_rename_siren_entreprise_siret"),
        ("clients", "0006_rename_siren_client_siret"),
    ]

    operations = [
        migrations.CreateModel(
            name="Document",
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
                ("is_draft", models.BooleanField(default=False)),
                ("document_number", models.CharField(max_length=255)),
                (
                    "forme",
                    models.CharField(
                        choices=[
                            ("facture", "Facture"),
                            ("devis", "Devis"),
                            ("avoir", "Avoir"),
                        ]
                    ),
                ),
                ("subject", models.CharField(max_length=255)),
                (
                    "payment_method",
                    models.CharField(
                        choices=[
                            ("bank_transfer", "Virement bancaire"),
                            ("check", "Chèque"),
                            ("cash", "Espèce"),
                            ("credit_card", "Carte bancaire"),
                            ("direct_debit", "Prélèvement automatique"),
                            ("other", "Autre"),
                        ]
                    ),
                ),
                ("validity_date", models.DateField()),
                ("payment_mention", models.CharField()),
                ("other_mention", models.CharField()),
                ("notes", models.TextField()),
                ("vat_payer", models.BooleanField()),
                ("total_ht", models.FloatField()),
                ("total_vat", models.FloatField()),
                ("total_ttc", models.FloatField()),
                (
                    "client",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="documents",
                        to="clients.client",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="documents",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "entreprise",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="documents",
                        to="entreprise.entreprise",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="DocumentSection",
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
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("section-title", "Titre"),
                            ("section-article", "Article"),
                            ("section-subtotal", "Sous-total"),
                        ]
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("unit_price_ht", models.FloatField()),
                ("quantity", models.FloatField()),
                ("vat_rate", models.FloatField()),
                (
                    "article_type",
                    models.CharField(
                        choices=[("service", "Service"), ("product", "Product")]
                    ),
                ),
                ("discount", models.FloatField()),
                (
                    "discount_type",
                    models.CharField(
                        choices=[("percentage", "Pourcentage"), ("amount", "Montant")]
                    ),
                ),
                ("discount_description", models.TextField()),
                (
                    "unit",
                    models.CharField(
                        choices=[
                            ("", "Aucune"),
                            ("mm", "mm"),
                            ("cm", "cm"),
                            ("m", "m"),
                            ("km", "km"),
                            ("m²", "m²"),
                            ("m³", "m³"),
                            ("kg", "kg"),
                            ("hour", "hour"),
                            ("day", "day"),
                            ("month", "month"),
                            ("year", "year"),
                            ("ml", "ml"),
                            ("l", "l"),
                        ],
                        default="",
                    ),
                ),
                ("display_price_infos", models.BooleanField(default=True)),
                (
                    "document",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sections",
                        to="documents.document",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]