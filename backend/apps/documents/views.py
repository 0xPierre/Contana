from datetime import datetime

from django.db.models import QuerySet

from services.constructor.generate import construct_pdf
from .models import Document, DocumentSection
from ..core.permissions import CanAccessDocuments, IsInEntreprise, CanAccessConstructor, IsEntrepriseBillingOk
from ..core.utils import get_entreprise_from_request
from .utils import generate_next_document_number
from django.db.models import Q
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import (
    action,
)
from rest_framework.permissions import IsAuthenticated

# from rest_framework.request import Request
from rest_framework.response import Response
from django.core.exceptions import PermissionDenied

from .pagination import DocumentsSetPagination
from .serializers import DocumentsDetailSerializer, DocumentsListingSerializer


class DocumentsViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and listing documents instance
    """

    pagination_class = DocumentsSetPagination
    permission_classes = [
        IsAuthenticated,
        IsInEntreprise,
        CanAccessDocuments,
        IsEntrepriseBillingOk,
    ]

    def get_serializer_class(self):
        if self.action == "list":
            return DocumentsListingSerializer

        return DocumentsDetailSerializer

    def get_queryset(self):
        queryset: QuerySet[Document] = get_entreprise_from_request(
            self.request
        ).documents.all()

        if self.request.query_params.get("search"):
            search = self.request.query_params.get("search")
            q_query = (
                Q(client__socialreasonorname__icontains=search)
                | Q(subject__icontains=search)
                | Q(other_mention__icontains=search)
                | Q(payment_mention__icontains=search)
                | Q(notes__icontains=search)
                | Q(document_number__icontains=search)
            )
            queryset = queryset.filter(q_query)

        if self.request.query_params.get(
            "start_date"
        ) and not self.request.query_params.get("end_date"):
            queryset = queryset.filter(
                created_at__date=datetime.strptime(
                    self.request.query_params.get("start_date"), "%d/%m/%Y"
                ).date(),
            )
        elif self.request.query_params.get(
            "start_date"
        ) and self.request.query_params.get("end_date"):
            queryset = queryset.filter(
                created_at__date__gte=datetime.strptime(
                    self.request.query_params.get("start_date"), "%d/%m/%Y"
                ).date(),
                created_at__date__lte=datetime.strptime(
                    self.request.query_params.get("end_date"), "%d/%m/%Y"
                ).date(),
            )

        if self.request.query_params.get("forme"):
            queryset = queryset.filter(forme=self.request.query_params.get("forme"))

        if self.request.query_params.get("state"):
            queryset = queryset.filter(state=self.request.query_params.get("state"))

        if self.request.query_params.get("sort_by"):
            if self.request.query_params.get("sort_desc") == "true":
                queryset = queryset.order_by(
                    f"-{self.request.query_params.get('sort_by')}"
                )
            else:
                queryset = queryset.order_by(
                    f"{self.request.query_params.get('sort_by')}"
                )

        return queryset

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsAuthenticated, IsInEntreprise],
    )
    def duplicate(self, *args, **kwargs):
        """
        Allows to duplicate a document
        """
        target_document: Document = self.get_object()
        new_document = Document(
            created_at=timezone.now(),
            updated_at=timezone.now(),
            is_draft=True,
            document_number=generate_next_document_number(
                target_document.entreprise, target_document.forme, True
            ),
            forme=target_document.forme,
            client=target_document.client,
            subject=target_document.subject,
            payment_method=target_document.payment_method,
            validity_date=target_document.validity_date,
            payment_mention=target_document.payment_mention,
            other_mention=target_document.other_mention,
            notes=target_document.notes,
            vat_payer=target_document.vat_payer,
            entreprise=target_document.entreprise,
            created_by=self.request.user,
            total_ht=target_document.total_ht,
            total_tva=target_document.total_tva,
            total_ttc=target_document.total_ttc,
            state="draft",
        )

        new_document.save()
        for section in target_document.sections.all():
            new_section = section
            new_section.pk = None
            new_section.document = new_document
            new_section.save()

        return Response(
            {
                "status": "success",
                "data": {
                    "id": new_document.id,
                    "document_number": new_document.document_number,
                },
            }
        )

    def retrieve(self, request, *args, **kwargs):
        """
        Allows to retrieve a document
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"status": "success", "data": serializer.data})

    def destroy(self, request, *args, **kwargs):
        """
        Allows to delete a document
        Only draft documents can be deleted and devis in produced state
        """
        instance: Document = self.get_object()

        can_be_deleted = False

        if instance.is_draft:
            can_be_deleted = True

        elif instance.forme == "devis" and instance.state == "produced":
            can_be_deleted = True

        if not can_be_deleted:
            raise PermissionDenied()

        instance.delete()
        return Response({"status": "success"})

    @action(detail=True, methods=["post"], url_path="state")
    def change_state(self, *args, **kwargs):
        """
        Allows to change the state of a document
        """
        instance: Document = self.get_object()

        state = self.request.data.get("state")

        if state == "devis_accepted" or state == "devis_refused":
            """
            Devis can be accepted or refused only if they are in produced state
            """
            if instance.forme != "devis" and instance.state != "produced":
                raise PermissionDenied()

            instance.state = state
            instance.devis_accepted_or_refused_at = timezone.now()

        elif state == "paid":
            """
            Facture or avoir can be paid only if they are in produced state
            """
            if (
                instance.forme != "facture" or instance.forme != "avoir"
            ) and instance.state != "produced":
                raise PermissionDenied()

            instance.state = state
            instance.paid_at = timezone.now()

            # if instance.forme == "facture" and instance.linked_devis:
            #     instance.linked_devis.state = "devis_invoiced"
            #     instance.linked_devis.save()

        instance.save()
        return Response({"status": "success"})

    @action(detail=True, methods=["post"], url_path="produce-facture-from-devis")
    def produce_facture_from_devis(self, *args, **kwargs):
        instance: Document = self.get_object()

        if (
            instance.forme != "devis"
            or instance.state != "devis_accepted"
            or hasattr(instance, "linked_facture")
        ):
            raise PermissionDenied()

        total_ht = instance.total_ht
        total_tva = instance.total_tva
        total_ttc = instance.total_ttc

        for acompte in instance.linked_acomptes.all():
            total_ht -= acompte.total_ht
            total_tva -= acompte.total_tva
            total_ttc -= acompte.total_ttc

        new_document = Document(
            document_number=generate_next_document_number(
                instance.entreprise, "facture", False
            ),
            forme="facture",
            client=instance.client,
            subject=instance.subject,
            payment_method=instance.payment_method,
            validity_date=instance.validity_date,
            payment_mention=instance.payment_mention,
            other_mention=instance.other_mention,
            notes=instance.notes,
            vat_payer=instance.vat_payer,
            entreprise=instance.entreprise,
            created_by=self.request.user,
            total_ht=total_ht,
            total_tva=total_tva,
            total_ttc=total_ttc,
            state="produced",
            linked_devis=instance,
        )

        new_document.save()

        for section in instance.sections.all():
            new_section = section
            new_section.pk = None
            new_section.document = new_document
            new_section.save()

        for acompte in instance.linked_acomptes.all():
            section = DocumentSection(
                type="section-article",
                title=f"Acompte sur devis n°{instance.document_number}",
                description="",
                unit_price_ht=-acompte.total_ht,
                total_ht=-acompte.total_ht,
                total_ht_without_discount=-acompte.total_ht,
                quantity=1,
                vat_rate=acompte.sections.first().vat_rate,
                article_type="service",
                document=new_document,
            )
            section.save()

        new_document.file = construct_pdf(new_document, new_document.sections.all())
        new_document.save()

        return Response(
            {
                "status": "success",
                "data": {
                    "document_id": new_document.id,
                    "document_number": new_document.document_number,
                },
            }
        )

    @action(detail=True, methods=["post"], url_path="produce-acompte-from-devis")
    def produce_acompte(self, *args, **kwargs):
        instance: Document = self.get_object()
        acompte_data = self.request.data.get("acompte", None)

        if (
            instance.forme != "devis"
            or instance.state != "devis_accepted"
            or not acompte_data
        ):
            raise PermissionDenied()

        if acompte_data["type"] != "percentage" and acompte_data["type"] != "amount":
            raise PermissionDenied()

        if instance.vat_payer and not acompte_data["vat_rate"] > 0:
            return Response(
                {
                    "status": "failed",
                    "error": "Veuillez renseigner un taux de TVA supérieur à 0%",
                }
            )

        # Verify if the total amount of the acomptes is not greater than the total amount of the devis
        total_ttc_acomptes = 0
        for acompte in instance.linked_acomptes.all():
            total_ttc_acomptes += acompte.total_ttc

        if acompte_data["type"] == "percentage":
            amount = round(instance.total_ttc * (float(acompte_data["value"]) / 100), 2)
        else:
            amount = round(float(acompte_data["value"]), 2)

        if total_ttc_acomptes + amount > instance.total_ttc:
            return Response(
                {
                    "status": "failed",
                    "error": "Le montant total des acomptes ne peut pas être supérieur au montant total du devis",
                }
            )

        if instance.vat_payer:
            amount_ttc = amount
            amount_ht = round(amount_ttc / (1 + (acompte_data["vat_rate"] / 100)), 2)
            amount_tva = round(amount_ttc - amount_ht, 2)
        else:
            amount_ttc = amount
            amount_ht = amount
            amount_tva = 0

        acompte = Document(
            document_number=generate_next_document_number(
                instance.entreprise, "acompte", False
            ),
            forme="acompte",
            client=instance.client,
            subject=instance.subject,
            payment_method=instance.payment_method,
            validity_date=instance.validity_date,
            payment_mention=instance.payment_mention,
            other_mention=instance.other_mention,
            notes=instance.notes,
            vat_payer=instance.vat_payer,
            entreprise=instance.entreprise,
            created_by=self.request.user,
            total_ht=amount_ht,
            total_tva=amount_tva,
            total_ttc=amount_ttc,
            state="produced",
            linked_parent_devis=instance,
        )
        acompte.save()

        section = DocumentSection(
            type="section-article",
            title=f"Acompte sur devis n°{instance.document_number}",
            description="",
            unit_price_ht=amount_ht,
            total_ht=amount_ht,
            total_ht_without_discount=amount_ht,
            quantity=1,
            vat_rate=acompte_data["vat_rate"],
            article_type="service",
            document=acompte,
        )
        section.save()

        acompte.file = construct_pdf(acompte, [section])
        acompte.save()

        return Response(
            {
                "status": "success",
                "data": {
                    "document_id": acompte.id,
                    "document_number": acompte.document_number,
                },
            }
        )
