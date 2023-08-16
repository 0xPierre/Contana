from .models import Entreprise
from rest_framework import serializers


class EntrepriseUpdateInformationsModelSerializer(serializers.ModelSerializer):
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
            "siret",
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
        if Entreprise.objects.filter(email=value).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError("Cet email est déjà utilisé")

        return value
