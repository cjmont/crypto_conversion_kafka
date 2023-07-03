import json
from notbank.base.utils.kafka.tramas.exceptions import TramaException
from notbank.transactions.models.deposit import Deposit
from notbank.transactions.models.user import User
from notbank.tasks.tasks.shared import is_instance_with_current_deposit, log_error_with_traceback, send_to_notbank_app_socket
from notbank.base.utils.kafka.tramas.notify_deposit_out import NotifyDeposit
from notbank.base.exceptions import RequestIDNotFoundException
from celery import shared_task
from django.conf import settings
from django.db import IntegrityError

from notbank.base.utils.kafka.producer import Producer
from notbank.base.utils.kafka.tramas.get_result_deposit_balance_manager_in import GetResultDepositBalanceManagerIn
from notbank.transactions.models.current_deposit import CurrentDeposit
from notbank.base.utils.parse_decimal import dec_to_str_striped
# get return fee


@shared_task
def get_result_deposit_notify(trama: str):
    try:
        # obtener trama desde el Balance Manager Engine
        data = GetResultDepositBalanceManagerIn.from_trama(trama)
        task_id = data.task_id
        status = data.status
        
    except TramaException as e:
        log_error_with_traceback(
            f'failed to read trama: {trama}. Exception: {e}')
        return  
    if is_instance_with_current_deposit(task_id):
        # comparar request_id con el task_id del result, si son iguales se notifica
        # Si request_id es igual al del task_id del balance Manager 
        # o existe en BD se genera la trama y se envia la notificacion          
        request_deposit = Deposit.objects.get(request_id=task_id)
        # Obtener uuid usuario
        user = User.objects.get(id=request_deposit.user_id)
        notify = NotifyDeposit.to_trama(task_id=str(request_deposit.request_id), status=status)
        
        # Enviar trama notify a notbank app socket
        send_socket = send_to_notbank_app_socket(str(user.uuid), str(request_deposit.request_id), status, 'deposit' )
        
        # Enviar PUSH notification
        Producer.send_kafka_message(
            topic=settings.KAFKA_PUSH_TOPIC,
            message=str(notify),
        )
    
        
    
