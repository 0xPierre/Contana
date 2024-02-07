from ..entreprise.models import Entreprise, EntrepriseLogo
from ..user.models import User
from django.conf import settings
from guardian.core import ObjectPermissionChecker


def build_invitation_link(entreprise, token) -> str:
    return settings.FRONTEND_URL + "/%s/rejoindre/%s" % (
        entreprise.slug,
        token,
    )


def get_entreprise_data(entreprise: Entreprise, user: User) -> dict:
    data = {
        "id": entreprise.id,
        "name": entreprise.name,
        "slug": entreprise.slug,
        "owner": entreprise.owner.id,
        "is_owner": entreprise.owner == user,
        "users": [],
        "email": entreprise.email,
        "phone": entreprise.phone,
        "country": entreprise.country,
        "city": entreprise.city,
        "zip_code": entreprise.zip_code,
        "address": entreprise.address,
        "num_rcs": entreprise.num_rcs,
        "vat_number": entreprise.vat_number,
        "iban": entreprise.iban,
        "bic": entreprise.bic,
        "bank": entreprise.bank,
        "ape": entreprise.ape,
        "forme": entreprise.forme,
        "siren": entreprise.siren,
        "capital": entreprise.capital,
        "logos": [],
        "user_permissions": {},
        "document_logo_size": entreprise.document_logo_size,
        "document_logo_margin_right": entreprise.document_logo_margin_right,
        "document_logo_margin_top": entreprise.document_logo_margin_top,
        "document_logo_margin_bottom": entreprise.document_logo_margin_bottom,
        "document_logo_used": None,
        "document_default_payment_method": entreprise.document_default_payment_method,
        "document_payment_mention": entreprise.document_payment_mention,
        "document_other_mention": entreprise.document_other_mention,
        "document_notes": entreprise.document_notes,
        "vat_payer": entreprise.vat_payer,
        "first_facture_number": entreprise.first_facture_number,
        "first_devis_number": entreprise.first_devis_number,
        "first_acompte_number": entreprise.first_acompte_number,
        "first_avoir_number": entreprise.first_avoir_number,
        "first_client_number": entreprise.first_client_number,
    }

    entreprise_permissions = entreprise._meta.permissions
    if user.has_perm("administrate", entreprise) or user == entreprise.owner:
        for permission in entreprise_permissions:
            data["user_permissions"][permission[0]] = True
    else:
        permission_checker = ObjectPermissionChecker(user)
        for permission in entreprise_permissions:
            data["user_permissions"][permission[0]] = permission_checker.has_perm(
                permission[0], entreprise
            )

    user: User
    for user in entreprise.users.all():
        user_data = {
            "id": user.id,
            "email": user.email,
            "full_name": user.get_full_name,
            "permissions": {},
            "avatar": "",
        }
        if user.avatar:
            user_data["avatar"] = user.avatar.url

        if user.has_perm("administrate", entreprise) or user == entreprise.owner:
            for permission in entreprise_permissions:
                user_data["permissions"][permission[0]] = True

        else:
            permission_checker = ObjectPermissionChecker(user)
            for permission in entreprise_permissions:
                user_data["permissions"][permission[0]] = permission_checker.has_perm(
                    permission[0], entreprise
                )

        data["users"].append(user_data)

    logo: EntrepriseLogo
    for logo in entreprise.entreprise_logos.all():
        data["logos"].append(
            {
                "id": logo.id,
                "url": logo.file.url,
                "name": logo.file.name.split(
                    "/",
                )[-1],
            }
        )

        if logo == entreprise.document_logo_used:
            data["document_logo_used"] = logo.id

    return data
