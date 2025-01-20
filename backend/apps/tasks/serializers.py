from rest_framework import serializers

from .models import Task, Labels


class TaskLabelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Labels
        fields = ["id", "label", "color"]


class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "due_date",
            "created_by",
            "assigned_to",
            "labels",
            "client",
            "checked",
        ]


class TaskDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["title", "description", "due_date", "checked"]
