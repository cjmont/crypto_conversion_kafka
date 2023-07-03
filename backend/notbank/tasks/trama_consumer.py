import traceback

from django.conf import settings
from notbank.tasks.tasks.get_result_deposit_notify import get_result_deposit_notify
from notbank.base.models.base import Log
from notbank.base.utils.kafka.tramas.exceptions import (
    TramaFormatException, TramaValidationException)
from notbank.base.utils.kafka.tramas.sync_task import SyncTask
from notbank.base.utils.kafka.tramas.trama_reader import validate_trama
from notbank.tasks.tasks import (#sync_commited_conversion,
                                 save_quote,
                                 sync_commited_transfer, sync_uncommited_transfer,
                                 update_conversion_status_quote_service,
                                 update_transaction_status, update_user, notify_transactions, get_return_fee_send_deposit)


class TramaConsumer:

    @staticmethod
    def consume_trama(trama: str, topic: str):
        try:
            # validate signature
            validate_trama(trama)
        except TramaValidationException:
            error_msg = f'invalid trama, wrong signature. {traceback.format_exc()}'
            Log.error(error_msg, service=Log.SERVICE.KAFKA_CONSUMER)
            return
        except TramaFormatException:
            error_msg = f'invalid trama, invalid format. {traceback.format_exc()}'
            Log.error(error_msg, service=Log.SERVICE.KAFKA_CONSUMER)
            return
        process_trama = {
            settings.KAFKA_NOTBANK_SYNC_TOPIC: TramaConsumer.consume_sync_message,
            settings.KAFKA_BALANCE_MANAGER_STATUS_TOPIC: update_transaction_status.delay,
            settings.KAFKA_USER_DATA_TOPIC: update_user.delay,
            settings.KAFKA_QUOTE_SERVICE_RESULT_TOPIC: update_conversion_status_quote_service.delay,
            settings.KAFKA_QUOTE_LISTENER_TOPIC: save_quote.delay,
            settings.KAFKA_NOTIFY_TRANSACTION_TOPIC: notify_transactions.delay,
            settings.KAFKA_RETURN_FEE_TOPIC: get_return_fee_send_deposit.delay,
            settings.KAFKA_BALANCE_MANAGER_TASK_TOPIC: get_result_deposit_notify.delay
        }
        try:
            process_trama[topic](trama)
        except KeyError:
            error_msg = f'unhandled topic {topic}'
            Log.error(error_msg, service=Log.SERVICE.KAFKA_CONSUMER)

    @staticmethod
    def consume_sync_message(trama: str):
        try:
            task = SyncTask.from_trama(trama)
        except TramaFormatException:
            error_msg = f'invalid trama, wrong format. {traceback.format_exc()}'
            Log.error(error_msg, service=Log.SERVICE.KAFKA_CONSUMER)
            return
        process_trama = {
            SyncTask.Transaction.TRANSFER: {
                SyncTask.Task.SYNC_COMMITED: sync_commited_transfer,
                SyncTask.Task.SYNC_UNCOMMITED: sync_uncommited_transfer,
            },
            SyncTask.Transaction.CONVERSION: {
                #SyncTask.Task.SYNC_COMMITED: sync_commited_conversion,
                SyncTask.Task.SYNC_UNCOMMITED: lambda x: None,
            }
        }
        try:
            process_trama[task.transaction][task.task].delay(trama)
        except KeyError:
            error_msg = f'unhandled sync message {task.transaction} - {task.task}'
            Log.error(error_msg, service=Log.SERVICE.KAFKA_CONSUMER)
