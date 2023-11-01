from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from django.http import HttpResponse
from django.core.files.base import ContentFile
from django.utils.text import slugify

from .utils import get_section_values
from apps.core.permissions import IsInEntreprise, CanAccessConstructor
from apps.core.utils import getEntrepriseFromRequest
from apps.documents.utils import generate_next_document_number
from apps.entreprise.models import Entreprise
from apps.documents.models import Document, DocumentSection, TemplateCategory, Template
from .serializers import TemplateCategoriesDetailSerializer
from services.constructor.generate import construct_pdf


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsInEntreprise, CanAccessConstructor])
def save_document_draft(request: Request, entreprise_slug: str):
    """
    Save a document as a draft to be completed later
    """
    entreprise = get_object_or_404(Entreprise, slug=entreprise_slug)
    # If draft isn't already created, create it
    if request.data.get("document_number"):
        document = entreprise.documents.get(
            document_number=request.data.get("document_number"),
        )
    else:
        document = Document(
            is_draft=True,
            entreprise=entreprise,
            document_number=generate_next_document_number(
                entreprise, request.data.get("forme"), True
            ),
            created_by=request.user,
            state="draft",
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
            section.total_ht = values["totalHT"]
            section.total_ht_without_discount = values["totalHTWithoutDiscount"]

        elif section.type == "section-subtotal":
            section.subtotal = values["subtotal"]

        section.save()

    return Response(
        {"status": "success", "data": {"document_number": document.document_number}}
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsInEntreprise, CanAccessConstructor])
def get_document_draft(request: Request, entreprise_slug: str, document_number: str):
    """
    Get data from the draft to edit it in constructor
    """
    entreprise = get_object_or_404(Entreprise, slug=entreprise_slug)
    document = get_object_or_404(
        entreprise.documents, document_number=document_number, is_draft=True
    )

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
@permission_classes([IsAuthenticated, IsInEntreprise, CanAccessConstructor])
def produce_document_preview(request: Request, entreprise_slug: str):
    """
    Used to produce the preview of a document from the constructor. Return the pdf file directly
    """
    entreprise = get_object_or_404(Entreprise, slug=entreprise_slug)

    parent_facture = None
    client = None
    if request.data.get("forme") == "avoir":
        parent_facture = entreprise.documents.get(
            document_number=request.data.get("parent_document_number")
        )
        client = parent_facture.client
    else:
        if request.data.get("client"):
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

    # Invert the sign of the total if the document is an avoir
    if document.forme == "avoir":
        document.total_ht = -document.total_ht
        document.total_tva = -document.total_tva
        document.total_ttc = -document.total_ttc

        # Link the avoir to the parent facture
        document.linked_parent_facture = parent_facture

    sections = []
    for section_data in request.data.get("sections"):
        values = section_data.get("values")
        section = DocumentSection(
            type=section_data.get("type"),
            title=values["title"],
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
            section.total_ht = values["totalHT"]
            section.total_ht_without_discount = values["totalHTWithoutDiscount"]

            if document.forme == "avoir":
                section.unit_price_ht = -section.unit_price_ht
                section.total_ht = -section.total_ht
                section.total_ht_without_discount = -section.total_ht_without_discount

        elif section.type == "section-subtotal":
            section.subtotal = values["subtotal"]

            if document.forme == "avoir":
                section.subtotal = -section.subtotal

        section.save()
        sections.append(section)

    pdf = construct_pdf(document, sections, True)

    response = HttpResponse(pdf.read(), content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="preview.pdf"'
    return response


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsInEntreprise, CanAccessConstructor])
def produce_document(request: Request, entreprise_slug: str):
    """
    Used to produce a document from the constructor
    """
    entreprise = get_object_or_404(Entreprise, slug=entreprise_slug)

    parent_facture = None
    if request.data.get("forme") == "avoir":
        parent_facture = entreprise.documents.get(
            document_number=request.data.get("parent_document_number")
        )
        client = parent_facture.client
    else:
        if not request.data.get("client"):
            return Response(
                {"status": "failed", "error": "Merci de sélectionner un client"}
            )

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
        state="produced",
    )

    # Invert the sign of the total if the document is an avoir
    if document.forme == "avoir":
        document.total_ht = -document.total_ht
        document.total_tva = -document.total_tva
        document.total_ttc = -document.total_ttc

        # Link the avoir to the parent facture
        document.linked_parent_facture = parent_facture

    # Suppression of the used draft
    if request.data.get("is_draft") and request.data.get("draft_document_number"):
        entreprise.documents.get(
            document_number=request.data.get("draft_document_number"), is_draft=True
        ).delete()

    document.save()

    sections = []
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
            section.total_ht = values["totalHT"]
            section.total_ht_without_discount = values["totalHTWithoutDiscount"]

            if document.forme == "avoir":
                section.unit_price_ht = -section.unit_price_ht
                section.total_ht = -section.total_ht
                section.total_ht_without_discount = -section.total_ht_without_discount

        elif section.type == "section-subtotal":
            section.subtotal = values["subtotal"]

            if document.forme == "avoir":
                section.subtotal = -section.subtotal

        section.save()
        sections.append(section)

    document.file = construct_pdf(document, sections)
    document.save()

    return Response(
        {
            "status": "success",
            "data": {
                "document_number": document.document_number,
                "document_id": document.id,
            },
        }
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsInEntreprise, CanAccessConstructor])
def get_catalog(request: Request, entreprise_slug: str):
    """
    Get the catalog of the entreprise, for sections with and without categories
    """
    entreprise = get_object_or_404(Entreprise, slug=entreprise_slug)

    data = {
        "templates_without_category": [],
        "categories": [],
        "categories_labels": [],
    }

    for category in entreprise.template_categories.all():
        data["categories_labels"].append(category.name)

        category_data = {
            "id": category.id,
            "name": category.name,
            "templates": [],
        }

        for template in category.templates.all():
            template_data = {
                "id": template.id,
                "name": template.name,
                "values": get_section_values(template.article),
                "category_id": category.id,
            }

            category_data["templates"].append(template_data)

        data["categories"].append(category_data)

    for template in entreprise.templates.exclude(category__isnull=False):
        template_data = {
            "id": template.id,
            "name": template.name,
            "values": get_section_values(template.article),
            "category_id": None,
        }

        data["templates_without_category"].append(template_data)

    return Response({"status": "success", "data": data})


class TemplateCategoriesViewSet(viewsets.ModelViewSet):
    """
    Viewset for the TemplateCategory model, creation, edition and deletion
    """

    serializer_class = TemplateCategoriesDetailSerializer
    permission_classes = [IsAuthenticated, IsInEntreprise, CanAccessConstructor]

    def get_queryset(self):
        return getEntrepriseFromRequest(self.request).template_categories.all()

    def create(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        entreprise = getEntrepriseFromRequest(request)

        category = serializer.save(
            entreprise=entreprise,
        )

        return Response(
            {
                "status": "success",
                "data": {
                    "id": category.id,
                    "name": category.name,
                    "templates": [],
                },
            }
        )

    def update(self, request: Request, *args, **kwargs):
        instance: TemplateCategory = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"status": "success"})


"""
Implementation of template create/update/delete without using viewsets
"""


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsInEntreprise, CanAccessConstructor])
def create_template(request: Request, entreprise_slug: str):
    """
    Used to create a template and assign it to a category/or not
    """
    entreprise = get_object_or_404(Entreprise, slug=entreprise_slug)
    data = request.data

    values = data.get("values")

    if not data.get("name"):
        return Response(
            {"status": "failed", "error": "Merci de donner un nom à l'article"}
        )

    category = None
    if data.get("category_id"):
        category = entreprise.template_categories.get(id=data.get("category_id"))

    article = DocumentSection(
        type="section-article",
        title=values["title"],
        description=values["description"],
        unit_price_ht=values["unitPriceHT"],
        quantity=values["quantity"],
        vat_rate=values["vatRate"],
        article_type=values["articleType"],
        discount=values["discount"],
        discount_type=values["discountType"],
        discount_description=values["discountDescription"],
        unit=values["unit"],
        display_price_infos=values["displayPriceInfos"],
    )
    article.save()

    template = Template(
        name=data.get("name"),
        category=category,
        article=article,
        entreprise=entreprise,
    )
    template.save()

    return Response(
        {
            "status": "success",
            "data": {
                "id": template.id,
                "name": template.name,
                "values": get_section_values(template.article),
                "category_id": template.category.id if template.category else None,
            },
        }
    )


@api_view(["PUT"])
@permission_classes([IsAuthenticated, IsInEntreprise, CanAccessConstructor])
def update_template(request: Request, entreprise_slug: str, template_id: int):
    """
    Used to update a template
    """
    entreprise = get_object_or_404(Entreprise, slug=entreprise_slug)
    data = request.data

    template = entreprise.templates.get(id=template_id)

    category = None
    if data.get("category_id"):
        category = entreprise.template_categories.get(id=data.get("category_id"))
    template.category = category

    values = data.get("values")

    if not data.get("name"):
        return Response(
            {"status": "failed", "error": "Merci de donner un nom à l'article"}
        )

    template.name = data.get("name")
    template.article.title = values["title"]
    template.article.description = values["description"]
    template.article.unit_price_ht = values["unitPriceHT"]
    template.article.quantity = values["quantity"]
    template.article.vat_rate = values["vatRate"]
    template.article.article_type = values["articleType"]
    template.article.discount = values["discount"]
    template.article.discount_type = values["discountType"]
    template.article.discount_description = values["discountDescription"]
    template.article.unit = values["unit"]
    template.article.display_price_infos = values["displayPriceInfos"]

    template.article.save()
    template.save()

    return Response(
        {
            "status": "success",
            "data": {
                "id": template.id,
                "name": template.name,
                "values": get_section_values(template.article),
                "category_id": template.category.id if template.category else None,
            },
        }
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsInEntreprise, CanAccessConstructor])
def delete_template(request: Request, entreprise_slug: str, template_id: int):
    """
    Used to delete a template
    """
    entreprise = get_object_or_404(Entreprise, slug=entreprise_slug)

    template = entreprise.templates.get(id=template_id)
    template.article.delete()
    template.delete()

    return Response({"status": "success"})
