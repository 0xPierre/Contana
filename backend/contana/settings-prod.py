from .settings import *
import os

SECRET_KEY = os.environ.get("SECRET_KEY")

FRONTEND_URL = ""
BACKEND_URL = "https://exemple.com"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": os.environ.get("DB_PORT"),
    }
}

DEBUG = False

ALLOWED_HOSTS = ["*"]


if "AWS_STORAGE_BUCKET_NAME" in os.environ:
    STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

    AWS_STORAGE_BUCKET_NAME = os.environ["AWS_STORAGE_BUCKET_NAME"]
    AWS_S3_REGION_NAME = os.environ["AWS_S3_REGION_NAME"]

    AWS_S3_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
    AWS_S3_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]

if "AWS_SES_ACCESS_KEY_ID" in os.environ:
    AWS_SES_ACCESS_KEY_ID = os.environ.get("AWS_SES_ACCESS_KEY_ID")
    AWS_SES_SECRET_ACCESS_KEY = os.environ.get("AWS_SES_SECRET_ACCESS_KEY")


STRIPE_PUBLIC_KEY = os.environ["STRIPE_PUBLIC_KEY"]
STRIPE_SECRET_KEY = os.environ["STRIPE_SECRET_KEY"]
STRIPE_SUCCESS_URL = (
    BACKEND_URL + "/api/web/join/create-entreprise?session_id={CHECKOUT_SESSION_ID}"
)
STRIPE_CANCEL_URL = FRONTEND_URL + "/rejoindre?cancelled=1"
STRIPE_WEBHOOK_SECRET = os.environ["STRIPE_WEBHOOK_SECRET"]

SIMPLE_JWT["SIGNING_KEY"] = SECRET_KEY


import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://90624539d13a42d09965a4701a6b1012@o4505218471559168.ingest.sentry.io/4505218476015616",
    integrations=[
        DjangoIntegration(),
    ],
    traces_sample_rate=1.0,
    send_default_pii=True,
)
