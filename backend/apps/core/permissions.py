from rest_framework import permissions

from .utils import getEntrepriseFromRequest


class IsOwnerOfEntreprise(permissions.BasePermission):
    """
    Verify that user is owner of entreprise
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            entreprise = getEntrepriseFromRequest(request)
            if entreprise:
                if entreprise.owner == request.user:
                    return True

        return False


class IsAdminOfEntreprise(permissions.BasePermission):
    """
    Verify that user is admin of entreprise
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            entreprise = getEntrepriseFromRequest(request)
            if entreprise:
                if request.user.has_perm("administrate", entreprise):
                    return True

        return False


class IsInEntreprise(permissions.BasePermission):
    """
    Verify that user is in entreprise
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            entreprise = getEntrepriseFromRequest(request)
            if entreprise:
                if request.user in entreprise.users.all():
                    return True

        return False

class HasPermissionsOf(permissions.BasePermission):
    def __init__(self, permission):
        self.permission = permission

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            entreprise = getEntrepriseFromRequest(request)
            if entreprise:
                if request.user.has_perm(
                    self.permission, entreprise
                ) or request.user.has_perm("administrate", entreprise):
                    return True

        return False
