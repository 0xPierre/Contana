from ..core.models import BaseModel
from ..entreprise.models import Entreprise
from django.db import models
from ..user.models import User
from ..clients.models import Client
from django.utils.timezone import now


class Labels(BaseModel):
    label = models.CharField(max_length=255, unique=True)
    color = models.CharField(max_length=255)

    entreprise = models.ForeignKey(
        Entreprise, on_delete=models.CASCADE, related_name="labels"
    )

    def __str__(self):
        return self.label

    class Meta:
        ordering = ["label"]


class Task(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)

    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="created_tasks"
    )
    assigned_to = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="assigned_tasks"
    )

    labels = models.ManyToManyField(Labels, related_name="tasks")

    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="tasks", null=True
    )
    checked = models.BooleanField(default=False)

    entreprise = models.ForeignKey(
        Entreprise, on_delete=models.CASCADE, related_name="tasks"
    )
    checked_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.checked and self.checked_at is None:
            self.checked_at = now()
        elif not self.checked:
            self.checked_at = None

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]
