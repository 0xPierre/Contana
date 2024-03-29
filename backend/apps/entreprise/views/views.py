import random
import string

from django.http import HttpResponse

from services.constructor.generate import construct_pdf
from apps.clients.utils import generate_next_client_number
from apps.core.permissions import (
    CanAdministrate,
    IsInEntreprise,
    IsOwnerOfEntreprise,
)
from apps.documents.utils import generate_next_document_number
from apps.entreprise.models import Entreprise, InvitationsLink
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.http import urlencode
from guardian.shortcuts import assign_perm, remove_perm
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from apps.entreprise.serializers import EntrepriseInformationsModelSerializer
from apps.entreprise.utils import build_invitation_link, get_entreprise_data
from apps.documents.models import Document, DocumentSection
from apps.clients.models import Client


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsInEntreprise])
def get_data(request: Request, entreprise_slug: str) -> Response:
    """
    Allows to get the entreprise data
    """
    entreprise = Entreprise.objects.get(slug=entreprise_slug)

    return Response(
        {"status": "success", "data": get_entreprise_data(entreprise, request.user)}
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsInEntreprise, CanAdministrate])
def update_entreprise_informations(request: Request, entreprise_slug: str) -> Response:
    """
    Allows to update the entreprise informations
    """

    entreprise = Entreprise.objects.get(slug=entreprise_slug)

    serializer = EntrepriseInformationsModelSerializer(
        data=request.data, instance=entreprise
    )

    if not serializer.is_valid():
        return Response({"status": "failed", "errors": serializer.errors})

    serializer.save()

    return Response(
        {"status": "success", "data": get_entreprise_data(entreprise, request.user)}
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsOwnerOfEntreprise])
def delete_entreprise(request: Request, entreprise_slug: str) -> Response:
    """
    Allows to delete an entreprise
    """
    entreprise = Entreprise.objects.get(slug=entreprise_slug)

    entreprise.delete()

    return Response(
        {
            "status": "success",
        }
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated, CanAdministrate])
def update_entreprise_logos(request: Request, entreprise_slug: str) -> Response:
    """
    Allows to update the entreprise logos
    """

    entreprise = Entreprise.objects.get(slug=entreprise_slug)
    logos_id = [int(logo_id) for logo_id in request.data.getlist("logos_id", None)]
    logos = request.FILES.getlist("logos", None)

    for logo in entreprise.entreprise_logos.all():
        if logo.id not in logos_id:
            logo.delete()

    for logo in logos:
        entreprise.entreprise_logos.create(file=logo)

    return Response(
        {"status": "success", "data": get_entreprise_data(entreprise, request.user)}
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsInEntreprise, CanAdministrate])
def remove_user_from_entreprise(
    request: Request, entreprise_slug: str, user_id: int
) -> Response:
    """
    Allows to remove a user from the entreprise
    """
    entreprise = Entreprise.objects.get(slug=entreprise_slug)

    """
    A user cannot remove itself
    """
    if request.user.id == user_id:
        raise PermissionDenied()

    user = entreprise.users.get(id=user_id)

    """
    If the user has the administrate permission, he cannot remove the owner or another user with the administrate permission
    """
    if user.has_perm("administrate", entreprise) and request.user != entreprise.owner:
        raise PermissionDenied()

    entreprise.users.remove(user)

    return Response(
        {
            "status": "success",
            "data": {"users": get_entreprise_data(entreprise, request.user)["users"]},
        }
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsInEntreprise, CanAdministrate])
def update_entreprise_user_permissions(
    request: Request, entreprise_slug: str, user_id: int
) -> Response:
    """
    Allows to update the entreprise user permissions
    """
    entreprise = Entreprise.objects.get(slug=entreprise_slug)
    """
    A user cannot edit its own permissions
    """
    if request.user.id == user_id:
        raise PermissionDenied()

    edited_user = entreprise.users.get(id=user_id)

    """
    If the user has the administrate permission, he cannot edit the permissions of the owner or of another user with the administrate permission
    """
    if (
        edited_user.has_perm("administrate", entreprise)
        and request.user != entreprise.owner
    ):
        raise PermissionDenied()

    permissions = request.data.get("permissions", None)

    if permissions["administrate"]:
        for permission in entreprise._meta.permissions:
            assign_perm(permission[0], edited_user, entreprise)
    else:
        for permission in entreprise._meta.permissions:
            remove_perm(permission[0], edited_user, entreprise)

        for permission in entreprise._meta.permissions:
            if permissions[permission[0]]:
                assign_perm(permission[0], edited_user, entreprise)
            else:
                remove_perm(permission[0], edited_user, entreprise)

    return Response({"status": "success", "data": {}})


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsInEntreprise, CanAdministrate])
def create_invitation_link(request: Request, entreprise_slug: str) -> Response:
    """
    Allows to create an invitation link
    """
    entreprise = Entreprise.objects.get(slug=entreprise_slug)

    invitation = InvitationsLink(
        entreprise=entreprise,
        created_by=request.user,
    )
    # Generate a random token
    # Check if the token is already used
    token = ""
    while True:
        token = "".join(random.choices(string.ascii_lowercase + string.digits, k=25))
        if not entreprise.invitations_links.filter(token=token).exists():
            break

    invitation.token = token
    invitation.created_by = request.user
    invitation.expiry_date = invitation.created_at + timezone.timedelta(hours=24)
    invitation.save()
    invitation_link = build_invitation_link(entreprise, token)

    return Response(
        {
            "status": "success",
            "data": {
                "invitation_link": invitation_link,
                "invitation_token": token,
            },
        }
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsInEntreprise, CanAdministrate])
def send_invitation_link_by_email(request: Request, entreprise_slug: str) -> Response:
    """
    Allows administrators to send invitations link by email
    """
    entreprise = Entreprise.objects.get(slug=entreprise_slug)

    invitation = InvitationsLink.objects.get(
        entreprise=entreprise, token=request.data.get("invitation_token")
    )

    if not request.data.get("email"):
        return Response(
            {"status": "failed", "error": "Vous devez spécifier une adresse email"}
        )

    template = render_to_string(
        "email/invitation_email.html",
        {
            "entreprise": entreprise,
            "url": build_invitation_link(entreprise, invitation.token),
        },
    )

    try:
        send_mail(
            "Invitation à rejoindre %s" % entreprise.name,
            "Vous avez été invité à rejoindre l'entreprise %s sur Contana"
            % entreprise.name,
            "Contana <noreply@contana.fr>",
            [request.data.get("email")],
            html_message=template,
        )
    except Exception as e:
        return Response(
            {
                "status": "failed",
                "error": "Une erreur est survenue lors de l'envoi de l'email",
            }
        )

    return Response({"status": "success"})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def get_invitation_link_info(request: Request, entreprise_slug: str) -> Response:
    """
    Allows to get the entreprise data
    """
    try:
        entreprise = Entreprise.objects.get(slug=entreprise_slug)
    except Entreprise.DoesNotExist:
        return Response(
            {
                "status": "failed",
                "error": "L'entreprise n'existe pas",
                "data": {"is_valid": False},
            }
        )

    try:
        invitation = entreprise.invitations_links.get(
            token=request.data.get("invitation_token"),
            used=False,
        )
    except InvitationsLink.DoesNotExist:
        return Response(
            {
                "status": "failed",
                "error": "Le lien d'invitation n'existe pas",
                "data": {"is_valid": False},
            }
        )

    if invitation.expiry_date < timezone.now():
        return Response(
            {
                "status": "failed",
                "error": "Le lien d'invitation a expiré",
                "data": {"is_valid": False},
            }
        )

    return Response(
        {
            "status": "success",
            "data": {
                "is_valid": True,
                "entreprise_name": entreprise.name,
                "already_in": request.user in entreprise.users.all(),
            },
        }
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def join_entreprise(request: Request, entreprise_slug: str) -> Response:
    """
    Allows to join an entreprise
    """
    entreprise = Entreprise.objects.get(slug=entreprise_slug)

    try:
        invitation: InvitationsLink = entreprise.invitations_links.get(
            token=request.data.get("invitation_token"), used=False
        )
    except InvitationsLink.DoesNotExist:
        return Response(
            {
                "status": "failed",
                "error": "Le lien d'invitation n'existe pas",
                "data": {"is_valid": False},
            }
        )

    if invitation.expiry_date < timezone.now():
        return Response(
            {
                "status": "failed",
                "error": "Le lien d'invitation a expiré",
                "data": {"is_valid": False},
            }
        )

    if request.user in entreprise.users.all():
        return Response(
            {
                "status": "failed",
                "error": "Vous êtes déjà dans cette entreprise",
                "data": {"is_valid": False},
            }
        )

    entreprise.users.add(request.user)
    entreprise.save()

    # Reset the user's permissions
    # if the user has already been in the entreprise
    for permission in entreprise._meta.permissions:
        remove_perm(permission[0], request.user, entreprise)

    invitation.used = True
    invitation.used_at = timezone.now()
    invitation.used_by = request.user
    invitation.save()

    return Response(
        {
            "status": "success",
        }
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@permission_classes([IsAuthenticated, IsInEntreprise, CanAdministrate])
def update_entreprise_document_personalisation(
    request: Request, entreprise_slug: str
) -> Response:
    """
    This method allows to update the entreprise document personalisation
    For instance the logo displayed on the document, his size, margin...
    And complementary information on the document
    """
    entreprise = Entreprise.objects.get(slug=entreprise_slug)

    entreprise.document_logo_size = request.data.get("document_logo_size", 300)
    entreprise.document_logo_margin_right = request.data.get(
        "document_logo_margin_right", 0
    )
    entreprise.document_logo_margin_top = request.data.get(
        "document_logo_margin_top", 0
    )
    entreprise.document_logo_margin_bottom = request.data.get(
        "document_logo_margin_bottom", 0
    )
    entreprise.document_default_payment_method = request.data.get(
        "document_default_payment_method", "bank_transfer"
    )
    entreprise.document_payment_mention = request.data.get(
        "document_payment_mention", None
    )
    entreprise.document_other_mention = request.data.get("document_other_mention", None)
    entreprise.document_notes = request.data.get("document_notes", None)
    entreprise.vat_payer = request.data.get("vat_payer", True)

    logo_used = request.data.get("document_logo_used", None)
    if logo_used:
        entreprise.document_logo_used = entreprise.entreprise_logos.get(id=logo_used)
    else:
        entreprise.document_logo_used = None

    first_facture_number = int(request.data.get("first_facture_number"))
    first_devis_number = int(request.data.get("first_devis_number"))
    first_avoir_number = int(request.data.get("first_avoir_number"))
    first_acompte_number = int(request.data.get("first_acompte_number"))
    first_client_number = int(request.data.get("first_client_number"))

    if (
        first_facture_number < 1
        or first_devis_number < 1
        or first_avoir_number < 1
        or first_acompte_number < 1
        or first_client_number < 1
    ):
        return Response(
            {
                "status": "failed",
                "error": "Le numéro de départ des documents/clients doit être supérieur à 0",
            }
        )

    if first_facture_number != entreprise.first_facture_number:
        if entreprise.documents.filter(forme="facture", is_draft=False).exists():
            return Response(
                {
                    "status": "failed",
                    "error": "Vous ne pouvez pas changer le premier numéro de facture si des factures ont déjà été "
                    "créées",
                }
            )
        entreprise.first_facture_number = first_facture_number

    if first_devis_number != entreprise.first_devis_number:
        if entreprise.documents.filter(forme="devis", is_draft=False).exists():
            return Response(
                {
                    "status": "failed",
                    "error": "Vous ne pouvez pas changer le premier numéro de devis si des devis ont déjà été "
                    "créés",
                }
            )
        entreprise.first_devis_number = first_devis_number

    if first_avoir_number != entreprise.first_avoir_number:
        if entreprise.documents.filter(forme="avoir", is_draft=False).exists():
            return Response(
                {
                    "status": "failed",
                    "error": "Vous ne pouvez pas changer le premier numéro d'avoir si des avoirs ont déjà été "
                    "créés",
                }
            )
        entreprise.first_avoir_number = first_avoir_number

    if first_acompte_number != entreprise.first_acompte_number:
        if entreprise.documents.filter(forme="acompte", is_draft=False).exists():
            return Response(
                {
                    "status": "failed",
                    "error": "Vous ne pouvez pas changer le premier numéro d'acompte si des acomptes ont déjà été "
                    "créées",
                }
            )
        entreprise.first_acompte_number = first_acompte_number

    if first_client_number != entreprise.first_client_number:
        if entreprise.clients.exists():
            return Response(
                {
                    "status": "failed",
                    "error": "Vous ne pouvez pas changer le premier numéro de client si des clients ont déjà été "
                    "créées",
                }
            )
        entreprise.first_client_number = first_client_number

    entreprise.save()

    return Response(
        {"status": "success", "data": get_entreprise_data(entreprise, request.user)}
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@permission_classes([IsAuthenticated, IsInEntreprise, CanAdministrate])
def get_document_personnalization_preview(
    request: Request, entreprise_slug: str
) -> HttpResponse:
    """
    Used to produce a preview of a document using the new personalisation
    """
    entreprise = Entreprise.objects.get(slug=entreprise_slug)
    entreprise.document_logo_size = request.data.get("document_logo_size", 300)
    entreprise.document_logo_margin_right = request.data.get(
        "document_logo_margin_right", 0
    )
    entreprise.document_logo_margin_top = request.data.get(
        "document_logo_margin_top", 0
    )
    entreprise.document_logo_margin_bottom = request.data.get(
        "document_logo_margin_bottom", 0
    )

    client = Client(
        client_number=generate_next_client_number(entreprise),
        socialreasonorname="Société Dupond",
        city="Paris",
        zip_code="75000",
        address="1 rue de la paix",
        country="France",
        vat_number="FR123456789",
        siren="123456789",
    )

    section = DocumentSection(
        title="Création d'un site internet",
        type="section-article",
        article_type="article",
        description="Développement du site internet de de la stratégie SEO",
        vat_rate=20,
        unit_price_ht=100,
        quantity=1,
        total_ht=100,
        total_ht_without_discount=100,
    )

    document = Document(
        entreprise=entreprise,
        document_number=generate_next_document_number(entreprise, "facture"),
        forme="facture",
        subject="Création d'un site internet",
        payment_method=request.data.get("document_default_payment_method"),
        validity_date=timezone.now(),
        payment_mention=request.data.get("document_payment_mention"),
        other_mention=request.data.get("document_other_mention"),
        notes=request.data.get("document_notes"),
        vat_payer=request.data.get("vat_payer"),
        total_ht=100,
        total_tva=20,
        total_ttc=120,
        client=client,
    )

    pdf = construct_pdf(document, [section], True)

    response = HttpResponse(pdf.read(), content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="preview.pdf"'
    return response
