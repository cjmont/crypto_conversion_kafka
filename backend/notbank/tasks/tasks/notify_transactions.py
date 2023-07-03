from decimal import Decimal
import json
from urllib import request
import uuid
from notbank.tasks.tasks.shared import is_instance_with_current_deposit, log_error_with_traceback
from notbank.base.utils.kafka.tramas.exceptions import TramaException
from notbank.transactions.models.user import User
from celery import shared_task
from django.conf import settings
from django.db import IntegrityError
from notbank.transactions.models.current_deposit import CurrentDeposit
from notbank.transactions.models.deposit import Deposit
from notbank.base.utils.kafka.producer import Producer
from notbank.base.utils.kafka.tramas.payment_listener_notify_transactions import PaymentListenerNotifyTransactions
from notbank.base.utils.kafka.tramas.get_fee_cryptomarket_out import GetFeeCryptoMarketOut
# notify transactions 
@shared_task
def notify_transactions(trama: str):
    try:
        # leemos la trama del topico -notify_transactions-
        data = PaymentListenerNotifyTransactions.from_trama(trama)     
        
        # obtener lista de transacciones
        js = json.dumps(data.__dict__)
        data_ = json.loads(js)
        task = data_['task'] 
        transactions = data_['transactions']
        user_uuid = data_['userId']
    except TramaException as e:
            log_error_with_traceback(f'failed to read trama: {trama}. Exception: {e}')
            return   
    
    
    # Obtenemos valores de las transacciones
    currency = ''
    total_amount = Decimal(0)    
    for native in transactions:      
        # Obtenemos el monto total de la transacciones
        amount = native['native']['amount']
        total_amount += Decimal(amount)            
        # Obtenemos la moneda de la transaccion
        currency = native['native']['currency']
        
    if native or amount :
        # obtener trama para el topico -get-fee-
        get_fee = GetFeeCryptoMarketOut.to_trama(currency, str(total_amount))         
        #obtener request_id de trama get_fee
        request_id = get_fee[57:93]
        
        # Guardar en BD user_id, request_id, currency, amount
        current_req = CurrentDeposit(task_id=request_id)
        current_req.save()
        # Buscamos el usuario
        user = User.objects.get(uuid=user_uuid)
        iduser = user.id
        notify = Deposit(uuid=str(uuid.uuid4()), request_id=request_id, currency=currency, amount=total_amount, user_id=iduser)
        notify.save()     
        if is_instance_with_current_deposit(request_id):
            # envio de trama al topico -get_fee-
            Producer.send_kafka_message(
                    topic=settings.KAFKA_TOPIC_GET_FEE,
                    message=str(get_fee),
            )
            

