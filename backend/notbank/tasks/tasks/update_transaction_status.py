from celery import shared_task
from django.conf import settings
from notbank.base.utils.kafka.producer import Producer
from notbank.base.utils.kafka.tramas.balance_manager_status import \
    BalanceManagerStatus
from notbank.base.utils.kafka.tramas.exceptions import TramaFormatException
from notbank.tasks.tasks.shared import (
    is_instance_with_current_conversion, is_instance_with_current_transfer,
    log_error_with_traceback,
    send_conversion_status_to_notbank_app_socket,
    send_current_conversion_id_to_quote_service,
    send_transfer_status_to_notbank_app_socket, should_send_to_quote_service)
from notbank.transactions.models import (BMStatusWaitingSyncTask, Conversion,
                                         Transfer)


def update_transfer_status(transaction_status: BalanceManagerStatus) -> bool:
    try:
        transfer: Transfer = Transfer.objects.get(
            request_id=transaction_status.task_id)
    except Transfer.DoesNotExist:
        return False
    status_mapping = {
        BalanceManagerStatus.STATUS.SUCCESS: Transfer.STATUS.SUCCESS,
        BalanceManagerStatus.STATUS.ERROR: Transfer.STATUS.ERROR,
    }
    transfer.status = status_mapping[transaction_status.status]
    transfer.save()
    if is_instance_with_current_transfer(transfer.request_id):
        send_transfer_status_to_notbank_app_socket(
            user_uuid=str(transfer.from_user.uuid),
            request_id=str(transfer.request_id),
            transfer_status=transfer.status
        )
        Producer.send_kafka_message(
            topic=settings.KAFKA_PUSH_TOPIC,
            # TODO: define trama
            message="",
        )
    return True


def update_conversion_status(transaction_status: BalanceManagerStatus) -> bool:
    try:
        conversion: Conversion = Conversion.objects.get(
            request_id=transaction_status.task_id)
    except Conversion.DoesNotExist:
        return False
    status_mapping = {
        BalanceManagerStatus.STATUS.SUCCESS: Conversion.STATUS.BM_SUCCESS_QS_PENDING,
        BalanceManagerStatus.STATUS.ERROR: Conversion.STATUS.BM_ERROR,
    }
    conversion.status = status_mapping[transaction_status.status]
    conversion.save()
    if is_instance_with_current_conversion(conversion.request_id):
        if conversion.status != Conversion.STATUS.BM_PENDING:
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
    return True


def make_bm_status_wait_sync_task(transaction_status) -> None:
    status_mapping = {
        BalanceManagerStatus.STATUS.SUCCESS: BMStatusWaitingSyncTask.STATUS.SUCCESS,
        BalanceManagerStatus.STATUS.ERROR: BMStatusWaitingSyncTask.STATUS.ERROR,
    }
    BMStatusWaitingSyncTask(
        request_id=transaction_status.task_id,
        status=status_mapping[transaction_status.status]
    ).save()


def update(transaction_status: BalanceManagerStatus):
    """updates an already existing transaction status,
    if does not updates, then caches (saves) the status until the transaction arrives.

    returns true if updates, false if caches
    """
    updated = update_transfer_status(transaction_status)
    if updated:
        return
    updated = update_conversion_status(transaction_status)
    if updated:
        return
    # if we get here, then there is no transfer or conversion yet, so we store the status until arrives.
    make_bm_status_wait_sync_task(transaction_status)


@shared_task
def update_transaction_status(trama: str):
    try:
        transaction_status = BalanceManagerStatus.from_trama(trama)
    except TramaFormatException:
        log_error_with_traceback('unable to save transaction status')
    update(transaction_status)
