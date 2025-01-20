from .models import Task, Labels
from ..core.permissions import CanAdministrate, IsInEntreprise
from rest_framework import viewsets, permissions
from .serializers import TaskLabelsSerializer, TaskListSerializer, TaskDetailSerializer
from ..core.utils import get_entreprise_from_request
from django.db.models import QuerySet, Q
from django.utils.timezone import now


class LabelViewset(viewsets.ModelViewSet):
    serializer_class = TaskLabelsSerializer
    queryset = Labels.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsInEntreprise]

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes.append(CanAdministrate)
        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        return get_entreprise_from_request(self.request).labels.all()

    def perform_create(self, serializer):
        serializer.save(entreprise=get_entreprise_from_request(self.request))


class TaskViewset(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsInEntreprise]

    def get_serializer_class(self):
        if self.action == "list":
            return TaskListSerializer
        return TaskDetailSerializer

    def perform_create(self, serializer):
        serializer.save(
            entreprise=get_entreprise_from_request(self.request),
            created_by=self.request.user,
            assigned_to=self.request.user,
        )

    def get_queryset(self):
        entreprise = get_entreprise_from_request(self.request)
        queryset: QuerySet[Task] = entreprise.tasks.all()

        user_id = self.request.query_params.get("user")
        if self.request.user.has_perm("administrate", entreprise) and user_id:
            queryset = queryset.filter(assigned_to__id=user_id)
        else:
            queryset = queryset.filter(assigned_to=self.request.user)

        if self.action == "list":
            search = self.request.query_params.get("search")
            if search:
                q_query = Q(title__unaccent__icontains=search) | Q(
                    description__unaccent=search
                )
                queryset = queryset.filter(q_query)

            completed = self.request.query_params.get("completed")
            if completed == "never":
                queryset = queryset.filter(checked=False)
            elif completed == "today":
                q_query = Q(checked=False) | Q(
                    checked=True, checked_at__date=now().date()
                )
                queryset = queryset.filter(q_query)

        return queryset