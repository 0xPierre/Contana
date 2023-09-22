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


class LinkedDocument(serializers.RelatedField):
    """
    Serializer for the linked document model
    """

    def to_representation(self, value):
        return {
            "id": value.id,
            "document_number": value.document_number,
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
    linked_facture = LinkedDocument(read_only=True)
    linked_devis = LinkedDocument(read_only=True)
    linked_acomptes = LinkedDocument(read_only=True, many=True)
    linked_parent_devis = LinkedDocument(read_only=True)
    linked_parent_facture = LinkedDocument(read_only=True)
    linked_avoirs = LinkedDocument(read_only=True, many=True)

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
            "linked_facture",
            "linked_devis",
            "linked_acomptes",
            "linked_parent_devis",
            "linked_parent_facture",
            "linked_avoirs",
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
            "linked_facture": {"read_only": True},
            "linked_devis": {"read_only": True},
            "linked_acomptes": {"read_only": True},
            "linked_parent_devis": {"read_only": True},
            "linked_parent_facture": {"read_only": True},
            "linked_avoirs": {"read_only": True},
        }
