from .settings import *
import os
import sentry_sdk

FRONTEND_URL = "https://app.contana.fr"
BACKEND_URL = "https://api.contana.fr"

DEBUG = False

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS += [
    "dbbackup",
]

DBBACKUP_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
DBBACKUP_STORAGE_OPTIONS = {
    "access_key": AWS_S3_ACCESS_KEY_ID,
    "secret_key": AWS_S3_SECRET_ACCESS_KEY,
    "bucket_name": os.environ.get('BACKUP_S3_BUCKET_NAME'),
    "default_acl": "private",
    "endpoint_url": AWS_S3_ENDPOINT_URL,
    "region_name": AWS_S3_REGION_NAME,
}
DBBACKUP_CLEANUP_KEEP = 14
DBBACKUP_SEND_EMAIL = True
DBBACKUP_ADMINS = [os.environ.get("ADMIN_EMAIL")]

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


CELERY_BEAT_SCHEDULE["backup_database"] = {
    "task": "contana.tasks.backup_database",
    "schedule": crontab(minute="*/2"),
}
