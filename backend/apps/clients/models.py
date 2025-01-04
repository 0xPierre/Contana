from ..core.models import BaseModel
from ..entreprise.models import Entreprise
from django.db import models
from ..user.models import User


class ClientFiles(BaseModel):
    file = models.FileField(upload_to="clients/files")
    client = models.ForeignKey(
        "clients.Client", on_delete=models.CASCADE, related_name="files"
    )

    def __str__(self):
        return self.file.name

    class Meta:
        ordering = ["created_at"]


class Client(BaseModel):
    socialreasonorname = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    zip_code = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    vat_number = models.CharField(max_length=255, null=True, blank=True)
    siren = models.CharField(max_length=255, null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    website = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        choices=[
            ("particulier", "Particulier"),
            ("professionnel", "Professionnel"),
        ],
    )

    client_number = models.CharField(max_length=255, null=True, blank=True)

    entreprise = models.ForeignKey(
        Entreprise, on_delete=models.CASCADE, related_name="clients"
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_clients'
    )

    archived = models.BooleanField(default=False)

    def __str__(self):
        return self.socialreasonorname

    class Meta:
        ordering = ["created_at"]
