from celery import shared_task
from django.conf import settings
from django.db import IntegrityError
from notbank.base.utils.kafka.producer import Producer
from notbank.tasks.tasks.shared import (
    get_bm_status_wating_sync_task, is_instance_with_current_conversion,
    log_error_with_traceback, send_conversion_status_to_notbank_app_socket,
    send_current_conversion_id_to_quote_service,
    should_send_to_notbank_app_socket, should_send_to_quote_service)
from notbank.transactions.models import (BMStatusWaitingSyncTask, Conversion,
                                         User)


@shared_task
def sync_commited_conversion(trama: str) -> None:
    try:
        conversion = Conversion.from_sync_task_trama(trama)
    except User.DoesNotExist as e:
        log_error_with_traceback(
            f'failed to load conversion from trama, user does not exists: {e}')
        return
    transaction_status = get_bm_status_wating_sync_task(
        request_id=conversion.request_id
    )
    status_mapping = {
        BMStatusWaitingSyncTask.STATUS.PENDING: Conversion.STATUS.BM_PENDING,
        BMStatusWaitingSyncTask.STATUS.SUCCESS: Conversion.STATUS.BM_SUCCESS_QS_PENDING,
        BMStatusWaitingSyncTask.STATUS.ERROR:   Conversion.STATUS.BM_ERROR,
    }
    conversion.status = status_mapping[transaction_status]
    try:
        conversion.save()
    except IntegrityError as e:
        log_error_with_traceback(
            f'failed to save conversion, request_id already in use: {e}')
        return
    if is_instance_with_current_conversion(conversion.request_id):
        if should_send_to_notbank_app_socket(conversion):
            send_conversion_status_to_notbank_app_socket(
                str(conversion.user.uuid),
                str(conversion.request_id),
                conversion.status)
        if should_send_to_quote_service(conversion):
            send_current_conversion_id_to_quote_service(conversion.request_id)
            Producer.send_kafka_message(
                topic=settings.KAFKA_PUSH_TOPIC,
                # TODO: define trama
                message="",
            )
