from ..user.models import User
from ..entreprise.models import Entreprise


def get_user_data(user: User) -> dict:
    data = {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "full_name": user.full_name,
        "avatar": user.avatar.url if user.avatar else None,
        "entreprises": [],
        "is_billing_ok": True
    }

    entreprise: Entreprise
    for entreprise in user.entreprises.all():
        data["entreprises"].append(
            {
                "id": entreprise.id,
                "name": entreprise.name,
                "slug": entreprise.slug,
                "stripe_payment_status": entreprise.stripe_payment_status,
            }
        )

        if entreprise.stripe_payment_status != "paid":
            data["is_billing_ok"] = False

    return data
