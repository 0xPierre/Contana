from django.db import models
from ..core.models import BaseModel
from ..clients.models import Client
from ..user.models import User
from ..entreprise.models import Entreprise


documents_type = [("facture", "Facture"), ("devis", "Devis"), ("avoir", "Avoir")]

payments_method = [
    ("bank_transfer", "Virement bancaire"),
    ("check", "Chèque"),
    ("cash", "Espèce"),
    ("credit_card", "Carte bancaire"),
    ("direct_debit", "Prélèvement automatique"),
    ("other", "Autre"),
]

sections_types = [
    ("section-title", "Titre"),
    ("section-article", "Article"),
    ("section-subtotal", "Sous-total"),
]

articles_types = [
    ("service", "Service"),
    ("product", "Product"),
]

discount_types = [
    ("percentage", "Pourcentage"),
    ("amount", "Montant"),
]


units = [
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
]


class DocumentSection(BaseModel):
    type = models.CharField(choices=sections_types)
    title = models.CharField(max_length=255, blank=True)

    # Only for section-article
    description = models.TextField(blank=True)
    unit_price_ht = models.FloatField(default=0)
    quantity = models.FloatField(default=1)
    vat_rate = models.FloatField(default=20)
    article_type = models.CharField(choices=articles_types, blank=False, null=False)
    discount = models.FloatField(default=0)
    discount_type = models.CharField(choices=discount_types, null=True)
    discount_description = models.TextField(blank=True)
    unit = models.CharField(choices=units, default="")
    display_price_infos = models.BooleanField(default=True)

    document = models.ForeignKey(
        "Document", on_delete=models.CASCADE, related_name="sections"
    )

    def __str__(self):
        return f"{self.type} - {self.title}"


class Document(BaseModel):
    is_draft = models.BooleanField(default=False)

    document_number = models.CharField(max_length=255)
    forme = models.CharField(choices=documents_type)
    subject = models.CharField(max_length=255)
    client = models.ForeignKey(
        Client, on_delete=models.SET_NULL, related_name="documents", null=True
    )
    payment_method = models.CharField(choices=payments_method)
    validity_date = models.DateField()
    payment_mention = models.CharField()
    other_mention = models.CharField()
    notes = models.TextField()
    vat_payer = models.BooleanField()

    entreprise = models.ForeignKey(
        Entreprise, on_delete=models.SET_NULL, related_name="documents", null=True
    )

    # Analytics
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="documents",
        null=True,
    )
    total_ht = models.FloatField()
    total_tva = models.FloatField()
    total_ttc = models.FloatField()

    def __str__(self):
        return f"{self.document_number} - {self.subject}"
