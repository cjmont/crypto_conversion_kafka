from celery import shared_task
from django.conf import settings
from notbank.base.exceptions import NotBankException
from notbank.base.utils.kafka.producer import Producer
from notbank.tasks.tasks.shared import (
    get_bm_status_wating_sync_task, is_instance_with_current_transfer, log_error_with_traceback,
    send_transfer_status_to_notbank_app_socket)
from notbank.transactions.models import (BMStatusWaitingSyncTask, Transfer)
from notbank.transactions.models.user import User



def is_not_pending_transfer(transfer: Transfer):
    return transfer.status != Transfer.STATUS.PENDING


@shared_task
def sync_commited_transfer(trama: str):
    try:
        transfer = Transfer.from_sync_task_trama(trama)
    except NotBankException as e:
        log_error_with_traceback(f'failed to sync transfer: {e}')
        return
    except User.DoesNotExist as e:
        log_error_with_traceback(f'failed to sync transfer: {e}')
        return
    if is_not_pending_transfer(transfer):
        log_error_with_traceback('transfer status must be pending')
        return
    transaction_status = get_bm_status_wating_sync_task(
        request_id=transfer.request_id)
    status_mapping = {
        BMStatusWaitingSyncTask.STATUS.PENDING: Transfer.STATUS.PENDING,
        BMStatusWaitingSyncTask.STATUS.SUCCESS: Transfer.STATUS.SUCCESS,
        BMStatusWaitingSyncTask.STATUS.ERROR: Transfer.STATUS.ERROR,
    }
    transfer.status = status_mapping[transaction_status]

    Transfer.objects.update_or_create(
        request_id=transfer.request_id,
        defaults={
            field.name: getattr(transfer, field.name)
            for field
            in transfer._meta.fields
            if field.name not in ['request_id', 'uuid', 'id', 'updated_at']
        })

    if is_instance_with_current_transfer(transfer.request_id) and is_not_pending_transfer(transfer):
        send_transfer_status_to_notbank_app_socket(
            user_uuid=str(transfer.from_user.uuid),
            request_id=str(transfer.request_id),
            transfer_status=transfer.status
        )
        Producer.send_kafka_message(
            topic=settings.KAFKA_PUSH_TOPIC,
            message="",  # TODO: convert to relevant trama
        )
