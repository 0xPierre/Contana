from rest_framework.authtoken.models import Token

from ..core.models import BaseModel, payments_method
from ..user.models import User
from autoslug import AutoSlugField
from django.db import models


class EntrepriseLogo(BaseModel):
    file = models.ImageField(upload_to="entreprises/logos/")
    entreprise = models.ForeignKey(
        "Entreprise", on_delete=models.CASCADE, related_name="entreprise_logos"
    )

    def __str__(self):
        return self.entreprise.name + " - " + self.file.name


class InvitationsLink(BaseModel):
    token = models.CharField(max_length=255)
    used = models.BooleanField(default=False)
    used_at = models.DateTimeField(null=True, blank=True)
    used_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="used_invitations_links",
        null=True,
    )
    expiry_date = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="created_invitations_links",
        null=True,
    )

    entreprise = models.ForeignKey(
        "Entreprise", on_delete=models.CASCADE, related_name="invitations_links"
    )

    def __str__(self):
        return self.token


class EntrepriseCheckoutSession(BaseModel):
    """
    This model is used to store the checkout session for the entreprise
    """
    session_id = models.CharField(max_length=255)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="checkout_sessions"
    )
    name = models.CharField(max_length=255)
    siren = models.CharField(max_length=255)
    email = models.EmailField()


payment_status_choices = (
    ("paid", "Paid"),
    ("failed", "Failed"),
    ("cancelled", "Cancelled"),
)


class Entreprise(BaseModel):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(
        populate_from="name", unique=True, null=True, always_update=True
    )
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owned_entreprises"
    )
    users = models.ManyToManyField(User, related_name="entreprises")

    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(null=True, blank=True, default="")

    country = models.CharField(null=True, blank=True, default="France")
    city = models.CharField(null=True, blank=True, default="")
    zip_code = models.CharField(null=True, blank=True, default="")
    address = models.CharField(null=True, blank=True, default="")

    num_rcs = models.CharField(null=True, blank=True, default="")
    vat_number = models.CharField(null=True, blank=True, default="")
    iban = models.CharField(null=True, blank=True, default="")
    bic = models.CharField(null=True, blank=True, default="")
    bank = models.CharField(null=True, blank=True, default="")
    ape = models.CharField(null=True, blank=True, default="")
    forme = models.CharField(null=True, blank=True, default="")
    siren = models.CharField(null=True, blank=True, default="")
    capital = models.CharField(null=True, blank=True, default="")

    # Document personnalization
    document_logo_size = models.IntegerField(default=300)
    document_logo_margin_right = models.IntegerField(default=0)
    document_logo_margin_top = models.IntegerField(default=0)
    document_logo_margin_bottom = models.IntegerField(default=0)
    document_logo_used = models.ForeignKey(
        EntrepriseLogo,
        null=True,
        on_delete=models.SET_NULL,
        related_name="used_by",
    )
    document_default_payment_method = models.CharField(
        choices=payments_method, default="bank_transfer"
    )
    document_payment_mention = models.CharField(
        blank=True, default="À réception de la facture"
    )
    document_other_mention = models.CharField(blank=True, default="")
    document_notes = models.TextField(
        blank=True,
        default="En cas de retard de paiement, il sera appliqué des pénalités et intérêts de retard suivant le taux "
        "minimum légal en vigueur, par mois de retard. En outre, une indemnité forfaitaire pour frais de "
        "recouvrement de 40€ sera due.",
    )
    vat_payer = models.BooleanField(default=True)

    first_facture_number = models.IntegerField(default=1)
    first_devis_number = models.IntegerField(default=1)
    first_acompte_number = models.IntegerField(default=1)
    first_avoir_number = models.IntegerField(default=1)
    first_client_number = models.IntegerField(default=1)

    stripe_subscription_id = models.CharField(blank=True)
    stripe_customer_id = models.CharField(blank=True)
    stripe_payment_status = models.CharField(choices=payment_status_choices, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        permissions = (
            ("administrate", "Allows to administrate the entreprise"),
            ("access_documents", "Allows to access the documents"),
            ("update_documents", "Allows to update the documents"),
            ("access_clients", "Allows to access the clients"),
            ("update_clients", "Allows to update the clients"),
            ("access_constructor", "Allows to access the constructeur"),
            ("access_dashboard", "Allows to access the dashboard"),
            ("access_crm", "Allows to access CRM features")
        )

class ApplicationToken(Token):
    user = models.ForeignKey(
        User,
        related_name="application_tokens",
        on_delete=models.CASCADE,
        verbose_name="User",
    )
    entreprise = models.ForeignKey(
        Entreprise,
        related_name="application_tokens",
        on_delete=models.CASCADE,
        verbose_name="Entreprise",
    )
    name = models.CharField(max_length=255, verbose_name="Name", blank=True)

    class Meta:
        verbose_name = "Application Token"
        verbose_name_plural = "Application Tokens"
        ordering = ["-created"]