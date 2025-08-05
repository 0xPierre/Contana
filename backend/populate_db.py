import django
django.setup()

from datetime import timedelta
import argparse
from guardian.shortcuts import assign_perm

from apps.user.models import User
from apps.entreprise.models import Entreprise
from apps.clients.models import Client

def add_user():
    """
    Create a first user in the database
    """

    User.objects.all().delete()
    user = User.objects.create_user(email="user@mail.com", password="password")
    print('User user@mail.com with password "password" created')


def add_entreprise():
    """
    Create a first entreprise in the database
    """
    Entreprise.objects.all().delete()
    entreprise = Entreprise.objects.create(name="Presta", owner=User.objects.first(), stripe_payment_status="paid")
    entreprise.save()

    entreprise.users.add(User.objects.first())
    assign_perm("administrate", User.objects.first(), entreprise)

    print(f"Entreprise {entreprise.name} created")

def add_client():
    """
    Create a first client in the database
    """
    Client.objects.all().delete()
    client = Client.objects.create(socialreasonorname="DUPOND", entreprise=Entreprise.objects.first(), siren="123456789", address="11 rue des champs élysées", city="Paris", zip_code="75008", country="France")
    print(f"Client {client.socialreasonorname} created")




add_user()
add_entreprise()
add_client()