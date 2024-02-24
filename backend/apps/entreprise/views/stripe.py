import random
import string

from django.http import HttpResponse
from django.shortcuts import redirect

from services.constructor.generate import construct_pdf
from apps.clients.utils import generate_next_client_number
from apps.core.permissions import (
    CanAdministrate,
    IsInEntreprise,
    IsOwnerOfEntreprise,
)
from apps.documents.utils import generate_next_document_number
from apps.entreprise.models import Entreprise, InvitationsLink, EntrepriseCheckoutSession
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
import stripe
from django.conf import settings


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_entreprise_checkout_session(request: Request) -> Response:
    """
    Allows to create a checkout session
    """
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price": settings.STRIPE_ENTREPRISE_SUBSCRIPTION_PRICE_ID,
                "quantity": 1,
            },
        ],
        mode="subscription",
        success_url=settings.FRONTEND_URL + "/accueil?type=entreprise-new-success",
        cancel_url=settings.FRONTEND_URL + "/creer-une-entreprise?status=cancelled",
        customer_email=request.data.get("email"),
        locale="fr",
    )

    # Save the session
    EntrepriseCheckoutSession.objects.create(
        session_id=session.id,
        owner=request.user,
        name=request.data.get("name"),
        siren=request.data.get("siren"),
        email=request.data.get("email"),
    )

    return Response({
        "status": "success",
        "url": session.url,
    })


@api_view(["POST"])
def stripe_entreprise_subscription_webhook(request: Request):
    """
    Allows to handle the stripe webhook for entreprise subscription
    """
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_ENTREPRISE_SUBSCRIPTION_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        checkout_session = EntrepriseCheckoutSession.objects.get(session_id=session.id)
        entreprise = Entreprise.objects.create(
            name=checkout_session.name,
            owner=checkout_session.owner,
            siren=checkout_session.siren,
            email=checkout_session.email,
            stripe_subscription_id=session.subscription,
            stripe_customer_id=session.customer,
            stripe_payment_status=session.payment_status,
        )

        entreprise.users.add(checkout_session.owner)
        assign_perm("administrate", checkout_session.owner, entreprise)

    elif event["type"] == "invoice.paid":
        invoice = event["data"]["object"]

        if Entreprise.objects.filter(stripe_subscription_id=invoice.subscription).exists():
            entreprise = Entreprise.objects.get(stripe_subscription_id=invoice.subscription)
            entreprise.stripe_payment_status = "paid"
            entreprise.save()

    elif event["type"] == "invoice.payment_failed":
        invoice = event["data"]["object"]

        if Entreprise.objects.filter(stripe_subscription_id=invoice.subscription).exists():
            entreprise = Entreprise.objects.get(stripe_subscription_id=invoice.subscription)
            entreprise.stripe_payment_status = "failed"
            entreprise.save()

    return HttpResponse(status=200)

