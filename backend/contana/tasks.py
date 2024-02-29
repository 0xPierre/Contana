from contana.celery import app
from celery.utils.log import get_task_logger
from django.core import management

logger = get_task_logger(name=__name__)


@app.task
def backup_database() -> None:
    """
    Task to backup the database
    """
    logger.info("Running backup database task...")
    management.call_command('dbbackup --noinput -z --clear')
    logger.info("Backup database task finished.")
