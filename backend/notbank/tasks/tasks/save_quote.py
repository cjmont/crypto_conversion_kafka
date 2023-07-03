from datetime import datetime
from celery import shared_task

from notbank.base.utils.kafka.tramas.exceptions import TramaFormatException
from notbank.tasks.tasks.shared import log_error_with_traceback
from notbank.transactions.models.quote import Quote


@shared_task
def save_quote(trama: str) -> None:
    try:
        execute_conversion_data = Quote.from_quote_listener_trama(
            trama)
    except TramaFormatException:
        log_error_with_traceback(
            f'failed to save conversion. invalid trama {trama}')
        return
    try:
        execute_conversion_data.save()
    except:
        log_error_with_traceback(
            f'failed to save conversion (request_id={execute_conversion_data.request_id})'
        )
        return
