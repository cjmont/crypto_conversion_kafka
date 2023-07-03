import json
from notbank.base.utils.kafka.tramas.exceptions import TramaException
from notbank.tasks.tasks.shared import is_instance_with_current_deposit, log_error_with_traceback
from notbank.transactions.models.user import User
from notbank.transactions.models.deposit import Deposit
from notbank.base.exceptions import RequestIDNotFoundException
from celery import shared_task
from django.conf import settings
from django.db import IntegrityError

from notbank.base.utils.kafka.producer import Producer
from notbank.base.utils.kafka.tramas.get_fee_return_cryptomarket_in import GetFeeReturnCryptoMarketIn
from notbank.transactions.models.current_deposit import CurrentDeposit
from notbank.base.utils.kafka.tramas.deposit_out import DepositTransaction
from notbank.base.utils.parse_decimal import dec_to_str_striped


@shared_task
def get_return_fee_send_deposit(trama: str):
    try:
        # obtener trama del topico -return_fee-
        data = GetFeeReturnCryptoMarketIn.from_trama(trama)
        js = json.dumps(data.__dict__)
        data_ = json.loads(js)
        request_id_return = data_['request_id']
        fee = data_['fee']
        # comparar request_id_return con request_id_get_fee   
    except TramaException as e:
        log_error_with_traceback(f'failed to read trama: {trama}. Exception: {e}')
        return    
    
    if is_instance_with_current_deposit(request_id_return):
    
        # Si request_id del get_fee es igual al del return_fee o existe en BD se genera la trama y se envia al balance manager
        request_id_current = Deposit.objects.get(request_id=request_id_return)
        user = User.objects.get(id=request_id_current.user_id)
        user_id = user.uuid
        deposit = DepositTransaction.to_trama(user_uuid=str(user_id), currency=request_id_current.currency, amount=str(dec_to_str_striped(request_id_current.amount)), fee=fee)
        
        # Enviar trama deposit a balance manager engine
        Producer.send_kafka_message(
            topic=settings.KAFKA_BALANCE_MANAGER_TASK_TOPIC,
            message=str(deposit),
        )
