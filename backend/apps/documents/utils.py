from ..entreprise.models import Entreprise
from ..documents.models import Document
from django.db.models.query import QuerySet


def generate_next_document_number(entreprise: Entreprise, forme: str, is_draft=False):
    """
    Generate the next document number
    """
    documents = entreprise.documents.all()
    if is_draft:
        identifier = "B-"
        documents = documents.filter(is_draft=True)
    elif forme == "devis":
        identifier = "D-"
    elif forme == "facture":
        identifier = "F-"
    elif forme == "avoir":
        identifier = "AV-"
    elif forme == "acompte":
        identifier = "AC-"
    else:
        raise Exception("Unknown document type")

    if not is_draft:
        documents = documents.filter(is_draft=False, forme=forme)

    if documents.count() == 0:
        if forme == "devis":
            return identifier + str(entreprise.first_devis_number).zfill(6)
        elif forme == "facture":
            return identifier + str(entreprise.first_facture_number).zfill(6)
        elif forme == "avoir":
            return identifier + str(entreprise.first_avoir_number).zfill(6)
        elif forme == "acompte":
            return identifier + str(entreprise.first_acompte_number).zfill(6)
        else:
            raise Exception("Unknown document type")

    last_document = documents.last()
    new_document_number = int(last_document.document_number.replace(identifier, "")) + 1

    return identifier + str(new_document_number).zfill(6)
