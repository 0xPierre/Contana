from contana.celery import app
from celery.utils.log import get_task_logger
import os

logger = get_task_logger(name=__name__)


@app.task
def backup_database() -> None:
    """
    Task to backup the database
    """
    logger.info("Running backup database task...")
    os.system("python manage.py dbbackup --noinput -z --clean")

    logger.info("Backup database task finished.")