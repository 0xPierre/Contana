from rest_framework import permissions

from .utils import get_entreprise_from_request


class IsOwnerOfEntreprise(permissions.BasePermission):
    """
    Verify that user is owner of entreprise
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            entreprise = get_entreprise_from_request(request)
            if entreprise:
                if entreprise.owner == request.user:
                    return True

        return False


class IsInEntreprise(permissions.BasePermission):
    """
    Verify that user is in entreprise
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            entreprise = get_entreprise_from_request(request)
            if entreprise:
                if request.user in entreprise.users.all():
                    return True

        return False


def test_user_permission(self, request, permission):
    if request.user.is_authenticated:
        entreprise = get_entreprise_from_request(request)
        if entreprise:
            if request.user.has_perm(permission, entreprise) or request.user.has_perm(
                "administrate", entreprise
            ):
                return True

    return False


class CanAdministrate(permissions.BasePermission):
    def has_permission(self, request, view):
        return test_user_permission(self, request, "administrate")


class CanAccessDashboard(permissions.BasePermission):
    def has_permission(self, request, view):
        return test_user_permission(self, request, "access_dashboard")


class CanAccessClients(permissions.BasePermission):
    def has_permission(self, request, view):
        return test_user_permission(self, request, "access_clients")


class CanUpdateClients(permissions.BasePermission):
    def has_permission(self, request, view):
        return test_user_permission(self, request, "update_clients")


class CanAccessDocuments(permissions.BasePermission):
    def has_permission(self, request, view):
        return test_user_permission(self, request, "access_documents")


class CanUpdateDocuments(permissions.BasePermission):
    def has_permission(self, request, view):
        return test_user_permission(self, request, "update_documents")


class CanAccessConstructor(permissions.BasePermission):
    def has_permission(self, request, view):
        return test_user_permission(self, request, "access_constructor")
    
class CanAccessCRM(permissions.BasePermission):
    def has_permission(self, request, view):
        return  test_user_permission(self, request, "access_crm")


class IsEntrepriseBillingOk(permissions.BasePermission):
    """
    Verify that entreprise is billing ok
    """

    def has_permission(self, request, view):
        entreprise = get_entreprise_from_request(request)
        if entreprise:
            if entreprise.stripe_payment_status == "paid":
                return True

        return False