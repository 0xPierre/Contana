from datetime import datetime

from django.db.models import QuerySet

from .models import Document
from ..core.permissions import CanAccessDocuments, IsInEntreprise, CanAccessConstructor
from ..core.utils import getEntrepriseFromRequest
from .utils import generate_next_document_number
from django.db.models import Q
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import (
    action,
    permission_classes as permission_classes_decorator,
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
    ]

    def get_serializer_class(self):
        if self.action == "list":
            return DocumentsListingSerializer

        return DocumentsDetailSerializer

    def get_queryset(self):
        queryset: QuerySet[Document] = getEntrepriseFromRequest(
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

    @action(detail=True, methods=["post"])
    @permission_classes_decorator([IsAuthenticated, IsInEntreprise])
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
    @permission_classes_decorator([IsAuthenticated, IsInEntreprise])
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
