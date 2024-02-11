from celery import shared_task
from django.utils import timezone

from contana.celery import app
from ..documents.models import Document

from celery.utils.log import get_task_logger

logger = get_task_logger(name=__name__)

@app.task
def devis_expiry_periodic_task():
    """
    Iterate over all the devis and check if they are expired
    If so, update their status to devis_expired
    """
    logger.info("Running expired devis periodic task...")
    number_of_expired_devis = 0
    for devis in Document.objects.filter(forme="devis", state="produced"):
        if devis.validity_date < timezone.now().date():
            devis.state = "devis_expired"
            devis.save()
            number_of_expired_devis += 1

    logger.info(f"Expired devis periodic task finished. {number_of_expired_devis} devis expired")
