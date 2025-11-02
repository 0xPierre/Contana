from django.db.models import QuerySet

from .models import ClientStatus
from ..clients.models import Client
from ..core.permissions import IsInEntreprise, CanAccessClients, CanUpdateClients, IsEntrepriseBillingOk
from ..core.utils import get_entreprise_from_request, PUBLIC_API_AUTHENTICATION_CLASSES
from ..core.permissions import test_user_permission
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
    authentication_classes = PUBLIC_API_AUTHENTICATION_CLASSES
    permission_classes = [IsAuthenticated, IsInEntreprise, CanAccessClients, IsEntrepriseBillingOk]

    def get_permissions(self):
        """
        Override permissions based on action.
        Update operations require CanUpdateClients instead of CanAccessClients.
        """
        if self.action in ['update', 'partial_update']:
            return [IsAuthenticated(), IsInEntreprise(), CanUpdateClients(), IsEntrepriseBillingOk()]
        return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):
        if self.action == "list":
            return ClientsListingSerializer

        return ClientsDetailSerializer

    def get_queryset(self):
        queryset: QuerySet[Client] = get_entreprise_from_request(
            self.request
        ).clients.all()

        if self.action == 'list':
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
                    | Q(siren__icontains=search)
                    | Q(note__icontains=search)
                    | Q(website__icontains=search)
                    | Q(type__icontains=search)
                    | Q(client_number__icontains=search)
                )
                queryset = queryset.filter(q_query)

            if self.request.query_params.get("status"):
                queryset = queryset.filter(status=self.request.query_params.get("status"))
            else:
                queryset = queryset.exclude(status=ClientStatus.ARCHIVED)
            
            if test_user_permission(self, self.request, "administrate"):
                if self.request.query_params.get("created_by") != "-1" and self.request.query_params.get("created_by") != None:
                    created_by = self.request.query_params.get("created_by")
                    queryset = queryset.filter(created_by_id=created_by)
            else:
                queryset = queryset.filter(created_by=self.request.user)

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

    def create(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        entreprise = get_entreprise_from_request(request)

        client = serializer.save(
            entreprise=entreprise,
            client_number=generate_next_client_number(entreprise),
            created_by=request.user,
        )

        return Response(
            {
                "status": "success",
                "data": serializer.data,
            }
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"status": "success", "data": serializer.data})

    def update(self, request: Request, *args, **kwargs):
        instance: Client = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"status": "success"})

    def destroy(self, request, *args, **kwargs):
        """
        Clients can't be deleted
        """
        raise PermissionDenied

    @action(
        detail=True,
        methods=["post"],
        url_path="files",
        permission_classes=[IsAuthenticated, IsInEntreprise, CanUpdateClients, IsEntrepriseBillingOk],
    )
    def save_file(self, *args, **kwargs):
        client = self.get_object()

        files_id = []
        if "files_id" in self.request.data:
            files_id = [int(file_id) for file_id in self.request.data["files_id"]]

        files = self.request.FILES.getlist("files", None)

        for file in client.files.all():
            if file.id not in files_id:
                file.delete()

        for file in files:
            client.files.create(file=file)

        return Response({"status": "success"})
