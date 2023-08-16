from ..entreprise.models import Entreprise
from django.http import HttpRequest


def getEntrepriseFromRequest(request: HttpRequest) -> Entreprise or None:
    """
    Get entreprise from request
    """

    if request.GET.get("entreprise_slug"):
        return Entreprise.objects.get(slug=request.GET.get("entreprise_slug"))

    if request.parser_context.get("kwargs"):
        if request.parser_context.get("kwargs").get("entreprise_slug"):
            return Entreprise.objects.get(
                slug=request.parser_context.get("kwargs").get("entreprise_slug")
            )

    return None
