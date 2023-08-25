from rest_framework import serializers

from .models import Document, DocumentSection
from ..clients.models import Client


class ClientsField(serializers.RelatedField):
    """
    Serializer for the Client model for listing with documents
    """

    def to_representation(self, value):
        return {
            "id": value.id,
            "socialreasonorname": value.socialreasonorname,
            "client_number": value.client_number,
        }


class DocumentsListingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Document model for listing
    """

    client = ClientsField(read_only=True)

    class Meta:
        model = Document
        fields = [
            "id",
            "document_number",
            "client",
            "forme",
            "created_at",
            "total_ht",
            "is_draft",
            "subject",
            "state",
        ]
        extra_kwargs = {
            "document_number": {"read_only": True},
            "client": {"read_only": True},
            "forme": {"read_only": True},
            "created_at": {"read_only": True},
            "total_ht": {"read_only": True},
            "is_draft": {"read_only": True},
            "subject": {"read_only": True},
            "state": {"read_only": True},
        }


class DocumentsDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for the Document model for detail view
    """

    client = ClientsField(read_only=True)

    class Meta:
        model = Document
        fields = [
            "id",
            "document_number",
            "client",
            "forme",
            "created_at",
            "total_ht",
            "is_draft",
            "subject",
            "state",
        ]
        extra_kwargs = {
            "document_number": {"read_only": True},
            "client": {"read_only": True},
            "forme": {"read_only": True},
            "created_at": {"read_only": True},
            "total_ht": {"read_only": True},
            "is_draft": {"read_only": True},
            "subject": {"read_only": True},
            "state": {"read_only": True},
        }
