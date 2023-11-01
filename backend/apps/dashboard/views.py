from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from django.db.models import Sum
from apps.core.permissions import IsInEntreprise, CanAccessDashboard
from apps.dashboard.utils import get_start_date_and_end_date_from_period

from apps.entreprise.models import Entreprise
from apps.documents.models import Document


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsInEntreprise, CanAccessDashboard])
def get_cards_data(request: Request, entreprise_slug: str):
    """
    Get the data for the cards in the dashboard.
    Get :
    - turnover
    - cash_collection
    - outstanding_quotations
    - outstanding_client_amount
    """
    entreprise = get_object_or_404(Entreprise, slug=entreprise_slug)

    start_date_, end_date = get_start_date_and_end_date_from_period(
        request.data.get("period"),
        request.data.get("start_date"),
        request.data.get("end_date"),
        entreprise,
    )

    turnover = (
        entreprise.documents.filter(
            forme__in=["facture", "acompte"],
            is_draft=False,
            created_at__gte=start_date_,
            created_at__lte=end_date,
        ).aggregate(turnover=Sum("total_ht"))["turnover"]
        or 0.0
    )

    cash_collection = (
        entreprise.documents.filter(
            forme__in=["facture", "acompte"],
            is_draft=False,
            paid_at__gte=start_date_,
            paid_at__lte=end_date,
        ).aggregate(cash_collection=Sum("total_ht"))["cash_collection"]
        or 0.0
    )

    outstanding_quotations = (
        entreprise.documents.filter(
            forme__in=["devis"],
            is_draft=False,
            state="produced",
            created_at__gte=start_date_,
            created_at__lte=end_date,
        ).aggregate(outstanding_quotations=Sum("total_ht"))["outstanding_quotations"]
        or 0.0
    )

    outstanding_client_amount = (
        entreprise.documents.filter(
            forme__in=["facture", "acompte"],
            is_draft=False,
            state="produced",
            created_at__gte=start_date_,
            created_at__lte=end_date,
        ).aggregate(outstanding_client_amount=Sum("total_ht"))[
            "outstanding_client_amount"
        ]
        or 0.0
    )

    return Response(
        {
            "status": "success",
            "data": {
                "turnover": turnover,
                "cash_collection": cash_collection,
                "outstanding_quotations": outstanding_quotations,
                "outstanding_client_amount": outstanding_client_amount,
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
def get_best_articles_chart(request: Request, entreprise_slug: str):
    """
    Get the data for the best articles chart
    Take the 10 best articles in the period
    """
    entreprise = get_object_or_404(Entreprise, slug=entreprise_slug)

    period = request.data.get("period")
    start_date, end_date = get_start_date_and_end_date_from_period(
        period,
        request.data.get("start_date"),
        request.data.get("end_date"),
        entreprise,
    )

    articles = {}

    for document in entreprise.documents.filter(
        forme__in=["facture", "acompte"],
        is_draft=False,
        created_at__gte=start_date,
        created_at__lte=end_date,
    ):
        for section in document.sections.all():
            if section.type == "section-article":
                if section.title not in articles:
                    articles[section.title] = 0
                articles[section.title] += section.unit_price_ht * section.quantity

    articles = sorted(articles.items(), key=lambda x: x[1], reverse=True)[:10]

    labels = [article[0] for article in articles]
    serie = [article[1] for article in articles]

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
def get_best_clients_chart(request: Request, entreprise_slug: str):
    """
    Get the data for the best clients chart
    Take the 10 best clients in the period
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
        forme__in=["facture", "acompte"],
        is_draft=False,
        created_at__gte=start_date,
        created_at__lte=end_date,
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
