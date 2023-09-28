from rest_framework import serializers
from ..documents.models import TemplateCategory


class TemplateCategoriesDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model for detail view
    """

    class Meta:
        model = TemplateCategory
        fields = [
            "id",
            "name",
        ]
