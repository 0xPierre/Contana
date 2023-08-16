from ..core.models import BaseModel
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
    phone = models.CharField(max_length=255, null=True, blank=True)

    country = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    zip_code = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    num_rcs = models.CharField(max_length=255, null=True, blank=True)
    vat_number = models.CharField(max_length=255, null=True, blank=True)
    iban = models.CharField(max_length=255, null=True, blank=True)
    bic = models.CharField(max_length=255, null=True, blank=True)
    bank = models.CharField(max_length=255, null=True, blank=True)
    ape = models.CharField(max_length=255, null=True, blank=True)
    forme = models.CharField(max_length=255, null=True, blank=True)
    siret = models.CharField(max_length=255, null=True, blank=True)
    capital = models.CharField(max_length=255, null=True, blank=True)

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
        )
