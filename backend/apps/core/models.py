from django.db import models
from django.utils import timezone

payments_method = [
    ("bank_transfer", "Virement bancaire"),
    ("check", "Chèque"),
    ("cash", "Espèce"),
    ("credit_card", "Carte bancaire"),
    ("direct_debit", "Prélèvement automatique"),
    ("other", "Autre"),
]


class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
