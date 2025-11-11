from .models import Entreprise, ApplicationToken
from rest_framework import serializers


class EntrepriseInformationsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entreprise
        fields = [
            "name",
            "email",
            "phone",
            "country",
            "city",
            "zip_code",
            "address",
            "num_rcs",
            "vat_number",
            "iban",
            "bic",
            "bank",
            "ape",
            "forme",
            "siren",
            "capital",
        ]
        extra_kwargs = {
            "name": {
                "error_messages": {
                    "blank": "La dénomination de l'entreprise est obligatoire"
                },
                "allow_blank": False,
            },
            "email": {
                "error_messages": {"blank": "L'email est obligatoire"},
                "allow_blank": False,
            },
        }

    def validate_email(self, value):
        if self.instance is None:
            if Entreprise.objects.filter(email=value).exists():
                raise serializers.ValidationError("Cet email est déjà utilisé")
            return value

        if Entreprise.objects.filter(email=value).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError("Cet email est déjà utilisé")

        return value

class ApplicationTokenSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = ApplicationToken
        fields = ["key", "name", "created", "user"]
        read_only_fields = ["key", "created"]

    def get_user(self, obj):
        if obj.user:
            return {
                "id": obj.user.id,
                "first_name": obj.user.first_name,
                "last_name": obj.user.last_name,
                "full_name": obj.user.full_name,
                "email": obj.user.email,
            }
        return None