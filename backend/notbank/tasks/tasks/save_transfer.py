
from celery import shared_task
from django.conf import settings
from notbank.base.utils.kafka.producer import Producer
from notbank.tasks.tasks.shared import get_bm_status_wating_sync_task, log_error_with_traceback
from notbank.transactions.models import BMStatusWaitingSyncTask, Transfer, CurrentTransfer


def is_instance_with_current_transfer(task_id: str) -> bool:
    try:
        CurrentTransfer.objects.get(task_id=task_id)
        return True
    except CurrentTransfer.DoesNotExist:
        return False


@shared_task
def save_transfer(trama: str):
    try:
        transfer = Transfer.from_sync_task_trama(trama)
        transaction_status = get_bm_status_wating_sync_task(
            task_id=transfer.task_id)
        status_mapping = {
            BMStatusWaitingSyncTask.STATUS.PENDING: Transfer.STATUS.PENDING,
            BMStatusWaitingSyncTask.STATUS.SUCCESS: Transfer.STATUS.SUCCESS,
            BMStatusWaitingSyncTask.STATUS.ERROR: Transfer.STATUS.ERROR,
        }
        transfer.status = status_mapping[transaction_status]
    except Exception as e:
        log_error_with_traceback(f'failed to build transfer: {e}')
        return
    try:
        transfer.save()
    except Exception as e:
        log_error_with_traceback(
            f'failed to save transfer: {transfer.task_id}. Exception: {e}')
        return

    if is_instance_with_current_transfer(transfer.task_id):
        Producer.send_kafka_message(
            topic=settings.KAFKA_PUSH_TOPIC,
            message="",  # TODO: convert to relevant trama
        )
