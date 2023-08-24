from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from django.shortcuts import get_object_or_404
from ..core.permissions import IsInEntreprise
from ..documents.utils import generate_next_document_number
from ..entreprise.models import Entreprise
from ..documents.models import Document, DocumentSection


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsInEntreprise])
def produce_document_overview(request: Request, entreprise_slug: str):
    entreprise = Entreprise.objects.get(slug=entreprise_slug)
    print(entreprise)

    return Response(
        {
            "status": "success",
        }
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsInEntreprise])
def save_document_draft(request: Request, entreprise_slug: str):
    """
    Save a document as a draft to be completed later
    """
    entreprise = get_object_or_404(Entreprise, slug=entreprise_slug)
    print(request.data.get("document_number"))
    # If draft isn't already created, create it
    if request.data.get("document_number"):
        document = entreprise.documents.get(
            document_number=request.data.get("document_number")
        )
    else:
        document = Document(
            is_draft=True,
            entreprise=entreprise,
            document_number=generate_next_document_number(
                entreprise, request.data.get("forme"), True
            ),
            created_by=request.user,
        )

    document.forme = request.data.get("forme")

    document.subject = request.data.get("subject")
    document.payment_method = request.data.get("payment_method")

    if not request.data.get("validity_date"):
        return Response(
            {"status": "failed", "error": "La date de validité est obligatoire"}
        )

    document.validity_date = datetime.strptime(
        request.data.get("validity_date")[0:10], "%d/%m/%Y"
    ).date()
    document.payment_mention = request.data.get("payment_mention")
    document.other_mention = request.data.get("other_mention")
    document.notes = request.data.get("notes")
    document.vat_payer = request.data.get("vat_payer")

    document.total_ht = request.data.get("total_ht")
    document.total_tva = request.data.get("total_tva")
    document.total_ttc = request.data.get("total_ttc")

    if request.data.get("client"):
        document.client = entreprise.clients.get(id=request.data.get("client")["id"])
    else:
        document.client = None

    document.save()
    document.sections.all().delete()

    for section_data in request.data.get("sections"):
        values = section_data.get("values")
        section = DocumentSection(
            type=section_data.get("type"),
            title=values["title"],
            document=document,
        )

        if section.type == "section-article":
            section.description = values["description"]
            section.unit_price_ht = values["unitPriceHT"]
            section.quantity = values["quantity"]
            section.vat_rate = values["vatRate"]
            section.article_type = values["articleType"]
            section.discount = values["discount"]
            section.discount_type = values["discountType"]
            section.discount_description = values["discountDescription"]
            section.unit = values["unit"]
            section.display_price_infos = values["displayPriceInfos"]

        section.save()

    return Response(
        {"status": "success", "data": {"document_number": document.document_number}}
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsInEntreprise])
def get_document_draft(request: Request, entreprise_slug: str, document_number: str):
    """
    Get data from the draft to edit it in constructor
    """
    entreprise = get_object_or_404(Entreprise, slug=entreprise_slug)
    document = entreprise.documents.get(document_number=document_number, is_draft=True)

    sections = []
    for section in document.sections.all():
        section_data = {
            "type": section.type,
            "values": {
                "title": section.title,
            },
        }

        if section.type == "section-article":
            section_data["values"]["description"] = section.description
            section_data["values"]["unitPriceHT"] = section.unit_price_ht
            section_data["values"]["quantity"] = section.quantity
            section_data["values"]["vatRate"] = section.vat_rate
            section_data["values"]["articleType"] = section.article_type
            section_data["values"]["discount"] = section.discount
            section_data["values"]["discountType"] = section.discount_type
            section_data["values"]["discountDescription"] = section.discount_description
            section_data["values"]["unit"] = section.unit
            section_data["values"]["displayPriceInfos"] = section.display_price_infos

        sections.append(section_data)

    data = {
        "document_number": document.document_number,
        "forme": document.forme,
        "subject": document.subject,
        "payment_method": document.payment_method,
        "validity_date": document.validity_date,
        "payment_mention": document.payment_mention,
        "other_mention": document.other_mention,
        "notes": document.notes,
        "vat_payer": document.vat_payer,
        "total_ht": document.total_ht,
        "total_tva": document.total_tva,
        "total_ttc": document.total_ttc,
        "client": {},
        "sections": sections,
    }

    if document.client:
        data["client"]["id"] = document.client.id
        data["client"]["socialreasonorname"] = document.client.socialreasonorname
        data["client"]["address"] = document.client.address
        data["client"]["zip_code"] = document.client.zip_code
        data["client"]["city"] = document.client.city
        data["client"]["country"] = document.client.country
        data["client"]["client_number"] = document.client.client_number

    return Response({"status": "success", "data": data})


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsInEntreprise])
def produce_document(request: Request, entreprise_slug: str):
    """
    Used to produce a document from the constructor
    """
    entreprise = get_object_or_404(Entreprise, slug=entreprise_slug)

    if not request.data.get("client"):
        return Response({"status": "failed", "error": "Merci de choisir un client"})

    client = entreprise.clients.get(id=request.data.get("client")["id"])

    document = Document(
        entreprise=entreprise,
        document_number=generate_next_document_number(
            entreprise, request.data.get("forme"), False
        ),
        client=client,
        forme=request.data.get("forme"),
        subject=request.data.get("subject"),
        payment_method=request.data.get("payment_method"),
        validity_date=datetime.strptime(
            request.data.get("validity_date")[0:10], "%d/%m/%Y"
        ).date(),
        payment_mention=request.data.get("payment_mention"),
        other_mention=request.data.get("other_mention"),
        notes=request.data.get("notes"),
        vat_payer=request.data.get("vat_payer"),
        total_ht=request.data.get("total_ht"),
        total_tva=request.data.get("total_tva"),
        total_ttc=request.data.get("total_ttc"),
        created_by=request.user,
    )

    return Response(
        {
            "status": "success",
        }
    )
