import traceback
from functools import singledispatch

from django.conf import settings
from notbank.transactions.models.current_deposit import CurrentDeposit
from notbank.base.models.base import Log
from notbank.base.utils.kafka.producer import Producer
from notbank.base.utils.kafka.tramas.notbank_socket import NotbankSocket
from notbank.base.utils.kafka.tramas.quote_service_internal_execute_in import \
    QuoteServiceInternalExecuteIn
from notbank.base.utils.time import get_timestamp
from notbank.transactions.models import (BMStatusWaitingSyncTask, Conversion, CurrentTransfer,
                                         CurrentConversion, Transfer)


def log_error_with_traceback(message: str):
    Log.error(message=f'{message}. {traceback.format_exc()}',
              service=Log.SERVICE.CELERY)


def log_error_unexpected(message: str):
    log_error_with_traceback(
        f'Unexpected error. {message}. {traceback.format_exc()}')


def get_bm_status_wating_sync_task(*, request_id: str) -> BMStatusWaitingSyncTask.STATUS:
    # returns pending by default, meaning there is no status waiting
    transaction_status = BMStatusWaitingSyncTask.STATUS.PENDING
    try:
        pending_status: BMStatusWaitingSyncTask = BMStatusWaitingSyncTask.objects.get(
            request_id=request_id
        )
        transaction_status = pending_status.status
        pending_status.delete()
    except BMStatusWaitingSyncTask.DoesNotExist:
        pass
    return transaction_status


def should_send_to_quote_service(conversion: Conversion):
    return conversion.status == Conversion.STATUS.BM_SUCCESS_QS_PENDING


@singledispatch
def should_send_to_notbank_app_socket(data) -> bool:
    return False


@should_send_to_notbank_app_socket.register
def _(conversion: Conversion) -> bool:
    return conversion.status == Conversion.STATUS.BM_ERROR or conversion.status == Conversion.STATUS.BM_SUCCESS_QS_PENDING


@should_send_to_notbank_app_socket.register
def _(transfer: Transfer) -> False:
    return transfer.status == Transfer.STATUS.ERROR or transfer.status == Transfer.STATUS.SUCCESS


def is_instance_with_current_conversion(request_id: str) -> bool:
    try:
        CurrentConversion.objects.get(request_id=request_id)
        return True
    except CurrentConversion.DoesNotExist:
        return False


def send_current_conversion_id_to_quote_service(request_id: str) -> None:
    trama_data = QuoteServiceInternalExecuteIn(
        timestamp=get_timestamp(),
        request_id=str(request_id),
    )
    Producer.send_kafka_message(
        topic=settings.KAFKA_QUOTE_SERVICE_TOPIC,
        message=trama_data.to_trama(),
    )


def send_conversion_status_to_notbank_app_socket(user_uuid: str, request_id: str, conversion_status: Conversion.STATUS):
    try:
        status_maapping = {
            Conversion.STATUS.BM_SUCCESS_QS_PENDING: 'success',
            Conversion.STATUS.BM_ERROR: 'error',
        }
        status = status_maapping[conversion_status]
    except KeyError:
        log_error_with_traceback('invalid conversion status, cannot send')
        return
    send_to_notbank_app_socket(
        user_uuid, request_id, status, event_name='conversion')


def send_transfer_status_to_notbank_app_socket(user_uuid: str, request_id: str, transfer_status:  Transfer.STATUS):
    try:
        status_maapping = {
            Transfer.STATUS.SUCCESS: 'success',
            Transfer.STATUS.ERROR: 'error',
        }
        status = status_maapping[transfer_status]
    except KeyError:
        log_error_with_traceback('invalid transfer status, cannot send')
        return
    send_to_notbank_app_socket(
        user_uuid, request_id, status, event_name='transfer')


def is_instance_with_current_deposit(task_id):
    try:     
        CurrentDeposit.objects.get(task_id=task_id)
        return True
    except CurrentDeposit.DoesNotExist:
        return False
    

def send_to_notbank_app_socket(user_uuid: str, request_id: str, status: str, event_name: str):
    trama_data = NotbankSocket(
        timestamp=get_timestamp(),
        user_uuid=user_uuid,
        event_name=event_name,
        data={
            'taskId': request_id,
            'status': status,
        })
    Producer.send_kafka_message(
        topic=settings.KAFKA_NOTBANK_APP_SOCKET_TOPIC,
        message=trama_data.to_trama(),
    )


def is_instance_with_current_transfer(request_id: str) -> bool:
    try:
        CurrentTransfer.objects.get(request_id=request_id)
        return True
    except CurrentTransfer.DoesNotExist:
        return False
