import random
import string

from ..core.permissions import (
    CanAdministrate,
    IsInEntreprise,
    IsOwnerOfEntreprise,
)
from ..entreprise.models import Entreprise, InvitationsLink
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

from .serializers import EntrepriseUpdateInformationsModelSerializer
from .utils import build_invitation_link, get_entreprise_data


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

    serializer = EntrepriseUpdateInformationsModelSerializer(
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
