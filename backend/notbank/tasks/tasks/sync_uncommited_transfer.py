from celery import shared_task
from notbank.base.exceptions import NotBankException
from notbank.tasks.tasks.shared import log_error_with_traceback
from notbank.transactions.models import Transfer
from notbank.transactions.models.user import User


@shared_task
def sync_uncommited_transfer(trama: str):
    try:
        transfer = Transfer.from_sync_task_trama(trama)
        transfer.save()
    except NotBankException as e:
        log_error_with_traceback(f'failed to sync transfer: {e}')
    except User.DoesNotExist as e:
        log_error_with_traceback(f'failed to sync transfer: {e}')
