from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from datetime import timedelta
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from apps.core.permissions import IsInEntreprise, CanAccessDashboard
from apps.dashboard.utils import get_start_date_and_end_date_from_period

from apps.entreprise.models import Entreprise


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsInEntreprise, CanAccessDashboard])
def get_cards_data(request: Request, entreprise_slug: str):
    """
    Get the data for the cards in the dashboard.
    Get :
    - signed_quotes
    - turnover
    - cash_collection
    - outstanding_quotations
    - outstanding_client_amount
    - discovery_calls
    - follow_up_calls
    - new_professional_clients
    - new_private_customers
    - clients_to_follow_up
    - total_outsdanding_quotes
    """
    entreprise = get_object_or_404(Entreprise, slug=entreprise_slug)

    start_date_, end_date = get_start_date_and_end_date_from_period(
        request.data.get("period"),
        request.data.get("start_date"),
        request.data.get("end_date"),
        entreprise,
    )

    signed_quotes = (
        entreprise.documents.filter(
            forme__in=["devis"],
            state="devis_accepted",
            is_draft=False,
            devis_accepted_or_refused_at__date__gte=start_date_,
            devis_accepted_or_refused_at__date__lte=end_date,
        ).aggregate(turnover=Sum("total_ht"))["turnover"]
        or 0.0
    )
    total_avoir = (
            entreprise.documents.filter(
                forme__in=["avoir"],
                is_draft=False,
                created_at__date__gte=start_date_,
                created_at__date__lte=end_date,
            ).aggregate(total_avoir=Sum("total_ht"))["total_avoir"]
            or 0.0
    )
    # It's already negative
    signed_quotes += total_avoir

    turnover = (
        entreprise.documents.filter(
            forme__in=["facture", "acompte"],
            is_draft=False,
            created_at__date__gte=start_date_,
            created_at__date__lte=end_date,
        ).aggregate(turnover=Sum("total_ht"))["turnover"]
        or 0.0
    )
    turnover += total_avoir

    cash_collection = (
        entreprise.documents.filter(
            forme__in=["facture", "acompte"],
            is_draft=False,
            paid_at__date__gte=start_date_,
            paid_at__date__lte=end_date,
        ).aggregate(cash_collection=Sum("total_ht"))["cash_collection"]
        or 0.0
    )
    cash_collection += total_avoir

    outstanding_client_amount = (
        entreprise.documents.filter(
            forme__in=["facture", "acompte"],
            is_draft=False,
            state="produced",
            created_at__date__gte=start_date_,
            created_at__date__lte=end_date,
        ).aggregate(outstanding_client_amount=Sum("total_ht"))[
            "outstanding_client_amount"
        ]
        or 0.0
    )

    discovery_calls = "-"
    follow_up_calls = "-"

    new_professional_clients = entreprise.clients.filter(
        created_at__date__gte=start_date_, created_at__date__lte=end_date, type="professionnel"
    ).count()

    new_private_customers = entreprise.clients.filter(
        created_at__date__gte=start_date_, created_at__date__lte=end_date, type="particulier"
    ).count()

    clients_to_follow_up = "-"

    total_outstanding_quotations = (
        entreprise.documents.filter(
            forme__in=["devis"],
            is_draft=False,
            state="produced",
        ).aggregate(outstanding_quotations=Sum("total_ht"))["outstanding_quotations"]
        or 0.0
    )

    return Response(
        {
            "status": "success",
            "data": {
                "signed_quotes": signed_quotes,
                "turnover": turnover,
                "cash_collection": cash_collection,
                "outstanding_client_amount": outstanding_client_amount,
                "discovery_calls": discovery_calls,
                "follow_up_calls": follow_up_calls,
                "new_professional_clients": new_professional_clients,
                "new_private_customers": new_private_customers,
                "clients_to_follow_up": clients_to_follow_up,
                "total_outstanding_quotations": total_outstanding_quotations,
            },
        }
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsInEntreprise, CanAccessDashboard])
def get_turnover_chart(request: Request, entreprise_slug: str):
    """
    Get the data for the turnover chart.
    """
    entreprise = get_object_or_404(Entreprise, slug=entreprise_slug)

    period = request.data.get("period")
    start_date, end_date = get_start_date_and_end_date_from_period(
        period,
        request.data.get("start_date"),
        request.data.get("end_date"),
        entreprise,
    )

    labels = []
    serie = []

    months = [
        "Jan",
        "Fév",
        "Mar",
        "Avr",
        "Mai",
        "Juin",
        "Jui",
        "Août",
        "Sep",
        "Oct",
        "Nov",
        "Déc",
    ]

    if period == "year" or period == "last_year":
        labels = months

        for month in range(1, 13):
            turnover = (
                entreprise.documents.filter(
                    forme__in=["facture", "acompte"],
                    is_draft=False,
                    created_at__month=month,
                    created_at__year=start_date.year,
                ).aggregate(turnover=Sum("total_ht"))["turnover"]
                or 0.0
            )
            serie.append(turnover)

    else:
        days = [
            start_date + timedelta(days=x)
            for x in range(((end_date + timedelta(days=1)) - start_date).days)
        ]

        if period == "year" or period == "last_year":
            for day in days:
                if months[day.month - 1] in labels:
                    labels.append("")
                else:
                    labels.append(months[day.month - 1])

        else:
            for day in days:
                labels.append(day.strftime("%d/%m/%Y"))

        for day in days:
            turnover = (
                entreprise.documents.filter(
                    forme__in=["facture", "acompte"],
                    is_draft=False,
                    created_at__date=day.date(),
                ).aggregate(turnover=Sum("total_ht"))["turnover"]
                or 0.0
            )
            serie.append(turnover)

    return Response(
        {
            "status": "success",
            "data": {
                "labels": labels,
                "series": [
                    {
                        "name": "Chiffre d'affaires",
                        "data": serie,
                    }
                ],
            },
        }
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsInEntreprise, CanAccessDashboard])
def get_best_clients_by_signed_quotes(request: Request, entreprise_slug: str):
    """
    Get the data for the 10 best clients by signed quotes
    """
    entreprise = get_object_or_404(Entreprise, slug=entreprise_slug)

    period = request.data.get("period")
    start_date, end_date = get_start_date_and_end_date_from_period(
        period,
        request.data.get("start_date"),
        request.data.get("end_date"),
        entreprise,
    )

    clients = {}

    for document in entreprise.documents.filter(
        forme__in=["devis"],
        state="devis_accepted",
        is_draft=False,
        devis_accepted_or_refused_at__gte=start_date,
        devis_accepted_or_refused_at__lte=end_date,
    ):
        if document.client.socialreasonorname not in clients:
            clients[document.client.socialreasonorname] = 0
        clients[document.client.socialreasonorname] += document.total_ht

    clients = sorted(clients.items(), key=lambda x: x[1], reverse=True)[:10]

    labels = [client[0] for client in clients]
    serie = [client[1] for client in clients]

    return Response(
        {
            "status": "success",
            "data": {
                "labels": labels,
                "serie": serie,
            },
        }
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsInEntreprise, CanAccessDashboard])
def get_best_user_by_signed_quotes(request: Request, entreprise_slug: str):
    """
    Get the data for the 10 best user by signed quotes
    """
    entreprise = get_object_or_404(Entreprise, slug=entreprise_slug)

    period = request.data.get("period")
    start_date, end_date = get_start_date_and_end_date_from_period(
        period,
        request.data.get("start_date"),
        request.data.get("end_date"),
        entreprise,
    )

    users = {}

    for user in entreprise.users.all():
        users[user.full_name] = 0
        for document in entreprise.documents.filter(
            forme__in=["devis"],
            state="devis_accepted",
            is_draft=False,
            devis_accepted_or_refused_at__gte=start_date,
            devis_accepted_or_refused_at__lte=end_date,
            created_by=user
        ):
            users[user.full_name] += document.total_ht


    labels = [user for user in users]
    serie = [users[user] for user in users]

    return Response(
        {
            "status": "success",
            "data": {
                "labels": labels,
                "serie": serie,
            },
        }
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsInEntreprise, CanAccessDashboard])
def get_outstanding_quote_by_commercial(request: Request, entreprise_slug: str):
    """
    Get the data for the 10 best user by signed quotes
    """
    entreprise = get_object_or_404(Entreprise, slug=entreprise_slug)
    users = {}

    for user in entreprise.users.all():
        users[user.full_name] = 0
        for document in entreprise.documents.filter(
            forme__in=["devis"],
            state="produced",
            is_draft=False,
            created_by=user
        ):
            users[user.full_name] += document.total_ht


    labels = [user for user in users]
    serie = [users[user] for user in users]

    return Response(
        {
            "status": "success",
            "data": {
                "labels": labels,
                "serie": serie,
            },
        }
    )
