from ..user.models import User
from rest_framework import serializers
from PIL import Image
from io import BytesIO


class UserRegistrationSerializer(serializers.Serializer):
    first_name = serializers.CharField(
        max_length=100, error_messages={"required": "Le prénom est obligatoire"}
    )
    last_name = serializers.CharField(
        max_length=100, error_messages={"required": "Le nom est obligatoire"}
    )
    email = serializers.EmailField()
    password = serializers.CharField(
        max_length=255,
        write_only=True,
        min_length=8,
        error_messages={
            "min_length": "Le mot de passe doit contenir au moins 8 caractères"
        },
    )

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Cete email est déjà utilisé")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
        )
        user.first_name = validated_data["first_name"]
        user.last_name = validated_data["last_name"]
        user.save()

        return user


class UserProfilUpdateSerializer(serializers.Serializer):
    first_name = serializers.CharField(
        max_length=100, error_messages={"required": "Le prénom est obligatoire"}
    )
    last_name = serializers.CharField(
        max_length=100, error_messages={"required": "Le nom est obligatoire"}
    )
    email = serializers.EmailField()
    avatar = serializers.ImageField(required=False)

    def validate_email(self, value):
        if User.objects.filter(email=value).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError("Cete email est déjà utilisé")
        return value

    def validate_avatar(self, value):
        if value is not None:
            image = Image.open(BytesIO(value.read()))
            image.verify()

        if value is not None and value.size > 1024 * 1024 * 2:
            raise serializers.ValidationError("L'image ne doit pas dépasser 2Mo")

        return value

    def update(self):
        self.instance.first_name = self.validated_data["first_name"]
        self.instance.last_name = self.validated_data["last_name"]
        self.instance.email = self.validated_data["email"]

        if self.validated_data.get("avatar"):
            self.instance.avatar = self.validated_data["avatar"]

        self.instance.save()

        return self.instance


class UserPasswordUpdateSerializer(serializers.Serializer):
    current_password = serializers.CharField(
        max_length=255,
    )
    new_password = serializers.CharField(
        max_length=255,
        min_length=8,
        error_messages={
            "min_length": "Le mot de passe doit contenir au moins 8 caractères"
        },
    )
    password_confirmation = serializers.CharField(
        max_length=255,
    )

    def validate_current_password(self, value):
        if not self.instance.check_password(value):
            raise serializers.ValidationError("Votre mot de passe actuel est incorrect")
        return value

    def validate_password_confirmation(self, value):
        if value != self.initial_data["new_password"]:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas")
        return value

    def update(self):
        self.instance.set_password(self.validated_data["new_password"])
        self.instance.save()

        return self.instance
