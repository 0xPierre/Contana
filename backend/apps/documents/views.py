from datetime import datetime

from django.db.models import QuerySet

from .models import Document
from ..core.permissions import HasPermissionsOf, IsInEntreprise
from ..core.utils import getEntrepriseFromRequest
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated

# from rest_framework.request import Request
from rest_framework.response import Response

from .pagination import DocumentsSetPagination
from .serializers import DocumentsDetailSerializer, DocumentsListingSerializer


class DocumentsViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and listing documents instance
    """

    pagination_class = DocumentsSetPagination

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

    @permission_classes(
        [IsAuthenticated, IsInEntreprise, HasPermissionsOf("access_documents")]
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"status": "success", "data": serializer.data})

    # @action(detail=True, methods=["post"])
    # @permission_classes(
    #     [IsAuthenticated, IsInEntreprise, HasPermissionsOf("update_clients")]
    # )
    # def archive(self, *args, **kwargs):
    #     client = self.get_object()
    #     client.archived = True
    #     client.save()
    #
    #     return Response({"status": "success"})
