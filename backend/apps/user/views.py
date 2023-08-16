from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.http import urlencode
from rest_framework.response import Response
from django.template.loader import render_to_string
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

from ..user.models import User
from .utils import get_user_data

from .serializers import (
    UserRegistrationSerializer,
    UserProfilUpdateSerializer,
    UserPasswordUpdateSerializer,
)


@api_view(["POST"])
def user_registration(request):
    """
    Allows a user to create an account
    """
    serializer = UserRegistrationSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.create(serializer.validated_data)

        data = {
            "auth": user.get_jwt_tokens(),
            "user": get_user_data(user),
        }

        return Response({"status": "success", "data": data})

    return Response({"status": "failed", "errors": serializer.errors})


@api_view(["POST"])
def user_login(request):
    """
    Allows a user to login
    """
    email = request.data.get("email")
    password = request.data.get("password")

    user = authenticate(email=email, password=password)

    if user is None:
        return Response(
            {"status": "failed", "error": "Adresse e-mail ou mot de passe incorrect"}
        )

    data = {
        "auth": user.get_jwt_tokens(),
        "user": get_user_data(user),
    }

    return Response({"status": "success", "data": data})


@api_view(["POST"])
def user_password_reset_request(request):
    """
    Allows a user to request a password reset
    """
    email = request.data.get("email")

    if not User.objects.filter(
        email=email,
    ).exists():
        return Response({"status": "failed", "error": "Adresse e-mail inconnue"})

    user = User.objects.get(email=email)

    token = default_token_generator.make_token(user)

    user.reset_token = token
    user.reset_token_expiration = timezone.now() + timezone.timedelta(hours=1)
    user.save()

    url = f"{settings.FRONTEND_URL}/reinitialisation-du-mot-de-passe?{urlencode({'token': token})}"

    template = render_to_string(
        "email/password_reset.html",
        {
            "user": user,
            "url": url,
        },
    )

    try:
        send_mail(
            "Réinitialisation du mot de passe",
            "Vous avez demandé à réinitialiser votre mot de passe",
            "Contana <noreply@contana.fr>",
            [user.email],
            html_message=template,
        )
    except Exception as e:
        return Response(
            {"status": "failed", "error": "Une erreur est survenue lors de l'envoi"}
        )

    return Response({"status": "success"})


@api_view(["POST"])
def user_password_reset(request):
    """
    Allows a user to reset his password
    """
    token = request.data.get("token")
    password = request.data.get("password")
    password_confirmation = request.data.get("password_confirmation")

    if not token:
        return Response({"status": "failed", "error": "Token invalide"})

    if not password:
        return Response({"status": "failed", "error": "Mot de passe invalide"})

    if password != password_confirmation:
        return Response(
            {"status": "failed", "error": "Les mots de passe ne correspondent pas"}
        )

    if not User.objects.filter(
        reset_token=token,
    ).exists():
        return Response({"status": "failed", "error": "Token invalide ou expiré"})

    user = User.objects.get(reset_token=token)

    if user.reset_token_expiration < timezone.now():
        return Response({"status": "failed", "error": "Token invalide ou expiré"})

    user.set_password(password)
    user.reset_token = None
    user.reset_token_expiration = None
    user.save()

    return Response({"status": "success"})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def user_profil_update(request):
    """
    Allows a user to update his profil
    """
    serializer = UserProfilUpdateSerializer(request.user, data=request.data)

    if not serializer.is_valid():
        return Response({"status": "failed", "errors": serializer.errors})

    user = serializer.update()

    return Response({"status": "success", "data": {"user": get_user_data(user)}})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def user_password_update(request):
    """
    Allows to update user password
    """
    serializer = UserPasswordUpdateSerializer(request.user, data=request.data)

    if not serializer.is_valid():
        return Response({"status": "failed", "errors": serializer.errors})

    serializer.update()

    return Response({"status": "success"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_data(request):
    """
    Get user data ( liste of entreprises... )
    """
    user = request.user

    data = {
        "user": get_user_data(user),
    }

    return Response({"status": "success", "data": data})
