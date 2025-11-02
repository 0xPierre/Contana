from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication

from apps.entreprise.models import ApplicationToken


class ApplicationTokenAuthentication(TokenAuthentication):
    model = ApplicationToken

    def authenticate_credentials(self, key):
        model = self.get_model()

        try:
            token: ApplicationToken = model.objects.get(key=key)
        except model.DoesNotExist as e:
            raise exceptions.AuthenticationFailed("Invalid token.") from e

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed("User inactive or deleted.")

        return token.user, token
    
    def authenticate(self, request):
        """
        Authenticate and verify that ApplicationToken's entreprise matches request entreprise.
        """
        auth_result = super().authenticate(request)
        
        if auth_result:
            user, token = auth_result
            # If using ApplicationToken, verify entreprise matches
            if isinstance(token, ApplicationToken):
                from apps.core.utils import get_entreprise_from_request
                request_entreprise = get_entreprise_from_request(request)
                
                # If request specifies an entreprise, verify it matches token's entreprise
                if request_entreprise and token.entreprise != request_entreprise:
                    raise exceptions.AuthenticationFailed(
                        "Token is not valid for this entreprise."
                    )
        
        return auth_result