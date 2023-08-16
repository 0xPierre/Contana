from django.urls import path

from . import views

urlpatterns = [
    path(
        "data",
        views.get_data,
        name="get_data",
    ),
    path(
        "settings/informations",
        views.update_entreprise_informations,
        name="update_entreprise_informations",
    ),
    path(
        "settings/delete",
        views.delete_entreprise,
        name="delete_entreprise",
    ),
    path(
        "settings/logos",
        views.update_entreprise_logos,
        name="update_entreprise_logos",
    ),
    path(
        "settings/user/<int:user_id>/permissions",
        views.update_entreprise_user_permissions,
        name="update_entreprise_user_permissions",
    ),
    path(
        "settings/user/<int:user_id>/remove",
        views.remove_user_from_entreprise,
        name="remove_user_from_entreprise",
    ),
    path(
        "settings/invitations/create",
        views.create_invitation_link,
        name="create_invitation_link",
    ),
    path(
        "settings/invitations/send-by-email",
        views.send_invitation_link_by_email,
        name="send_invitation_link_by_email",
    ),
    path(
        "settings/invitations/get-info",
        views.get_invitation_link_info,
        name="get_invitation_link_info",
    ),
    path(
        "settings/invitations/join",
        views.join_entreprise,
        name="join_entreprise",
    ),
]
