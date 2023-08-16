from typing import List

from ..clients.models import Client
from ..core.permissions import HasPermissionsOf, IsInEntreprise
from ..core.utils import getEntrepriseFromRequest
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from .pagination import ClientsSetPagination
from .serializers import ClientsDetailSerializer, ClientsListingSerializer
from .utils import generate_next_client_number


class ClientsViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing client instances.
    """

    pagination_class = ClientsSetPagination

    def get_serializer_class(self):
        if self.action == "list":
            return ClientsListingSerializer

        return ClientsDetailSerializer

    def get_queryset(self):
        queryset: List[Client] = getEntrepriseFromRequest(self.request).clients.all()

        if self.request.query_params.get("search"):
            search = self.request.query_params.get("search")
            q_query = (
                Q(socialreasonorname__icontains=search)
                | Q(email__icontains=search)
                | Q(phone__icontains=search)
                | Q(country__icontains=search)
                | Q(city__icontains=search)
                | Q(zip_code__icontains=search)
                | Q(address__icontains=search)
                | Q(vat_number__icontains=search)
                | Q(siret__icontains=search)
                | Q(note__icontains=search)
                | Q(website__icontains=search)
                | Q(type__icontains=search)
                | Q(client_number__icontains=search)
            )
            queryset = queryset.filter(q_query)

        if self.request.query_params.get("archived"):
            if self.request.query_params.get("archived") == "true":
                queryset = queryset.filter(archived=True)
            else:
                queryset = queryset.filter(archived=False)

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
        [IsAuthenticated, IsInEntreprise, HasPermissionsOf("access_clients")]
    )
    def create(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        entreprise = getEntrepriseFromRequest(request)

        client = serializer.save(
            entreprise=entreprise,
            client_number=generate_next_client_number(entreprise),
        )

        return Response(
            {
                "status": "success",
                "data": serializer.data,
            }
        )

    @permission_classes(
        [IsAuthenticated, IsInEntreprise, HasPermissionsOf("access_clients")]
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"status": "success", "data": serializer.data})

    @permission_classes(
        [IsAuthenticated, IsInEntreprise, HasPermissionsOf("update_clients")]
    )
    def update(self, request: Request, *args, **kwargs):
        instance: Client = self.get_object()

        if instance.archived:
            raise PermissionDenied

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"status": "success"})

    def destroy(self, request, *args, **kwargs):
        """
        Clients can't be deleted
        """
        raise PermissionDenied

    @action(detail=True, methods=["post"])
    @permission_classes(
        [IsAuthenticated, IsInEntreprise, HasPermissionsOf("update_clients")]
    )
    def archive(self, *args, **kwargs):
        client = self.get_object()
        client.archived = True
        client.save()

        return Response({"status": "success"})

    @action(detail=True, methods=["post"])
    @permission_classes(
        [IsAuthenticated, IsInEntreprise, HasPermissionsOf("update_clients")]
    )
    def unarchive(self, *args, **kwargs):
        client = self.get_object()
        client.archived = False
        client.save()

        return Response({"status": "success"})

    @action(detail=True, methods=["post"], url_path="files")
    @permission_classes(
        [IsAuthenticated, IsInEntreprise, HasPermissionsOf("update_clients")]
    )
    def savefile(self, *args, **kwargs):
        client = self.get_object()

        files_id = [
            int(file_id) for file_id in self.request.data.getlist("files_id", None)
        ]
        files = self.request.FILES.getlist("files", None)

        for file in client.files.all():
            if file.id not in files_id:
                file.delete()

        for file in files:
            client.files.create(file=file)

        return Response({"status": "success"})
