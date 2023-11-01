from datetime import datetime, timedelta

from apps.entreprise.models import Entreprise


def get_start_date_and_end_date_from_period(
    period: str, start_date: str, end_date: str, entreprise: Entreprise
):
    """
    Get the start date and the end date from a period.
    """
    if period == "custom" and start_date and end_date:
        return datetime.strptime(start_date, "%d/%m/%Y"), datetime.strptime(
            end_date, "%d/%m/%Y"
        )

    start_date = None
    end_date = None
    if period == "week":
        today = datetime.today()
        start_date = today - timedelta(days=today.weekday())
        end_date = start_date + timedelta(days=6)

    elif period == "last_week":
        today = datetime.today()
        start_date = today - timedelta(days=today.weekday() + 7)
        end_date = start_date + timedelta(days=6)

    elif period == "month":
        today = datetime.today()
        start_date = datetime(today.year, today.month, 1)
        end_date = datetime(today.year, today.month + 1, 1) - timedelta(days=1)

    elif period == "last_month":
        today = datetime.today()
        start_date = datetime(today.year, today.month - 1, 1)
        end_date = datetime(today.year, today.month, 1) - timedelta(days=1)

    elif period == "year":
        today = datetime.today()
        start_date = datetime(today.year, 1, 1)
        end_date = datetime(today.year, 12, 31)

    elif period == "last_year":
        today = datetime.today()
        start_date = datetime(today.year - 1, 1, 1)
        end_date = datetime(today.year - 1, 12, 31)

    elif period == "all":
        start_date = entreprise.created_at
        end_date = datetime.today()

    else:
        raise Exception("Invalid period")

    return start_date, end_date
