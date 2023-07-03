from celery import shared_task
from django.conf import settings
from notbank.base.utils.kafka.producer import Producer
from notbank.tasks.tasks.shared import log_error_with_traceback
from notbank.transactions.models import Transfer, TransferRequest, User


@shared_task
def save_or_update_transfer_request(trama: str):
    try:
        transfer_request = TransferRequest.from_sync_task(trama)
    except User.DoesNotExist as e:
        log_error_with_traceback(f'{e}')
        return
    try:
        saved_transfer_request: TransferRequest = TransferRequest.objects.get(
            task_id=transfer_request.task_id)
        try:
            Transfer.objects.get(task_id=transfer_request.transfer.task_id)
        except Exception as e:
            log_error_with_traceback(f'transfer should not exists: {e}')
            return
        saved_transfer_request.status = transfer_request.status
        saved_transfer_request.save()
    except TransferRequest.DoesNotExist as e:
        transfer_request.transfer.save()
        transfer_request.save()
    except Exception as e:
        log_error_with_traceback(f'unexpected exception: {e}')
        return
    Producer.send_kafka_message(
        topic=settings.KAFKA_PUSH_TOPIC,
        # TODO: define trama
        message="",
    )
