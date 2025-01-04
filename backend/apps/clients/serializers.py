from rest_framework import serializers

from .models import Client


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    full_name = serializers.CharField()
    email = serializers.CharField()


class ClientsListingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Client model for listing
    """
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Client
        fields = [
            "id",
            "socialreasonorname",
            "email",
            "phone",
            "country",
            "city",
            "zip_code",
            "address",
            "client_number",
            "created_at",
            "archived",
            "created_by",
        ]


class ClientsFilesField(serializers.RelatedField):
    """
    Serializer for a Client's file
    """

    def to_representation(self, value):
        return {
            "id": value.id,
            "url": value.file.url,
        }


class ClientsDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for the Client model for detail view
    """

    files = ClientsFilesField(many=True, read_only=True)
    document_count = serializers.SerializerMethodField()
    created_by = UserSerializer(required=False)

    @staticmethod
    def get_document_count(obj):
        return obj.documents.exclude(is_draft=True).count()

    def update(self, instance, validated_data):
        if 'created_by' in validated_data:
            created_by_data = validated_data.pop('created_by')
            instance.created_by_id = created_by_data.get('id')
        return super().update(instance, validated_data)

    class Meta:
        model = Client
        fields = [
            "id",
            "socialreasonorname",
            "email",
            "phone",
            "country",
            "city",
            "zip_code",
            "address",
            "vat_number",
            "siren",
            "type",
            "note",
            "website",
            "client_number",
            "created_at",
            "updated_at",
            "archived",
            "files",
            "document_count",
            "created_by",
        ]
        extra_kwargs = {
            "socialreasonorname": {
                "error_messages": {
                    "blank": "La raison sociale ou le nom du client est obligatoire"
                },
                "allow_blank": False,
            },
            "files": {"read_only": True},
            "read_only": ["client_number", "created_at", "updated_at"],
        }
