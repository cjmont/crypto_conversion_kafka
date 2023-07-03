from celery import shared_task
from django.db import DatabaseError
from notbank.base.models.base import Log

from notbank.transactions.models.quote import Quote


@shared_task
def delete_quotes_until(date: str):
    try:
        delete_created_at = Quote.objects.filter(created_at__lte=date)
        delete_created_at.delete()
        return Log.info(f"Deletion of quotes until {date}", Log.SERVICE.DELETE_OLD_QUOTE_CRON)
    except DatabaseError:
        return Log.error(f"Failed to delete quotes until {date}", Log.SERVICE.DELETE_OLD_QUOTE_CRON)
