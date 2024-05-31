from django.contrib import admin
from apps.entreprise.models import Entreprise, EntrepriseLogo, InvitationsLink, EntrepriseCheckoutSession, Entreprise

# Register your models here.
admin.site.register(Entreprise)
admin.site.register(EntrepriseLogo)
admin.site.register(InvitationsLink)
admin.site.register(EntrepriseCheckoutSession)
