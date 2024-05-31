from django.contrib import admin
from apps.clients.models import ClientFiles, Client

# Register your models here.
admin.site.register(Client)
admin.site.register(ClientFiles)