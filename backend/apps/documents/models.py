from django.db import models
from ..core.models import BaseModel, payments_method
from ..clients.models import Client
from ..user.models import User
from ..entreprise.models import Entreprise


documents_type = [
    ("facture", "Facture"),
    ("devis", "Devis"),
    ("avoir", "Avoir"),
    ("acompte", "Acompte"),
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
    ("", ""),
    ("mm", "mm"),
    ("cm", "cm"),
    ("m", "m"),
    ("km", "km"),
    ("m²", "m²"),
    ("m³", "m³"),
    ("kg", "kg"),
    ("hour", "heure(s)"),
    ("day", "jour(s)"),
    ("month", "mois"),
    ("year", "année(s)"),
    ("ml", "ml"),
    ("l", "l"),
]

states = [
    ("draft", "Brouillon"),
    ("produced", "Produit"),
    ("devis_accepted", "Devis accepté"),
    ("devis_refused", "Devis refusé"),
    ("devis_expired", "Devis expiré"),
    ("devis_invoiced", "Devis facturé"),
    ("paid", "Facture ou acompte payée"),
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
    total_ht = models.FloatField(default=0)
    total_ht_without_discount = models.FloatField(default=0)

    # Only for section-subtotal
    subtotal = models.FloatField(default=0)

    # null == True only when section is from a template
    document = models.ForeignKey(
        "Document",
        on_delete=models.CASCADE,
        related_name="sections",
        null=True,
    )
    entreprise = models.ForeignKey(
        Entreprise,
        on_delete=models.CASCADE,
        related_name="document_sections",
        null=True,
    )

    @property
    def get_unit(self):
        return dict(units)[self.unit]

    def __str__(self):
        return f"{self.type} - {self.title}"

    class Meta:
        ordering = ['id']


class TemplateCategory(BaseModel):
    name = models.CharField(max_length=255)

    entreprise = models.ForeignKey(
        Entreprise,
        on_delete=models.CASCADE,
        related_name="template_categories",
        null=True,
    )


class Template(BaseModel):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        TemplateCategory, on_delete=models.CASCADE, related_name="templates", null=True
    )

    article = models.ForeignKey(
        DocumentSection,
        on_delete=models.CASCADE,
        related_name="templates",
        null=True,
    )
    entreprise = models.ForeignKey(
        Entreprise, on_delete=models.CASCADE, related_name="templates", null=True
    )


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

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="documents",
        null=True,
    )
    total_ht = models.FloatField()
    total_tva = models.FloatField()
    total_ttc = models.FloatField()

    devis_accepted_or_refused_at = models.DateTimeField(null=True, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    state = models.CharField(choices=states, default="draft")

    linked_devis = models.OneToOneField(
        "Document",
        on_delete=models.SET_NULL,
        related_name="linked_facture",
        null=True,
        blank=True,
    )

    # used for acomptes
    linked_parent_devis = models.ForeignKey(
        "Document",
        on_delete=models.SET_NULL,
        related_name="linked_acomptes",
        null=True,
        blank=True,
    )

    # used for avoirs
    linked_parent_facture = models.ForeignKey(
        "Document",
        on_delete=models.SET_NULL,
        related_name="linked_avoirs",
        null=True,
        blank=True,
    )

    file = models.FileField(upload_to="documents", null=True, blank=True)

    @property
    def get_payment_method(self):
        return dict(payments_method)[self.payment_method]

    @property
    def get_forme(self):
        return dict(documents_type)[self.forme]

    def generate_pdf(self):
        from services.constructor.generate import construct_pdf
        self.file = construct_pdf(self, self.sections.all())
        self.save()

    def __str__(self):
        return f"{self.document_number} - {self.subject}"
