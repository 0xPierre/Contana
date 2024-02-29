from .settings import *
import os

FRONTEND_URL = "https://app.contana.fr"
BACKEND_URL = "https://api.contana.fr"

DEBUG = False

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS += [
    "dbbackup",
]

DBBACKUP_STORAGE = "django.core.files.storage.FileSystemStorage"
DBBACKUP_STORAGE_OPTIONS = {"location": "/home/0xpierre/contana-backups/"}


import sentry_sdk

sentry_sdk.init(
    dsn="https://b9046e239e1ef90b46226ada8fc9848a@o492474.ingest.sentry.io/4506728355725312",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)