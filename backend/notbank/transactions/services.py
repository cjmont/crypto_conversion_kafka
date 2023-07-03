import uuid
from decimal import Decimal
from http.client import OK
from typing import List, Optional

from django.conf import settings
from django.db import IntegrityError
from notbank.transactions.models.current_deposit import CurrentDeposit
from notbank.base.exceptions import (ConversionAlreadyRunningException, DepositAlreadyRunningException, QuoteNotFoundException, NotBankKafkaException,
                                     TransferRequestAlreadyCommitedException,
                                     TransferRequestNotFoundException, UserNotFoundException)
from notbank.base.utils.kafka.producer import Producer
from notbank.base.utils.kafka.tramas.nanobanco_quote import NanoBancoQuote
from notbank.base.utils.time import datetime_from_timestamp, get_timestamp
from notbank.transactions.models import (
    CurrentConversion, CurrentTransfer, Quote, Transfer, TransferRequest, User)
from notbank.transactions.models.conversion import Conversion


def new_transfer(
    from_user: str,
    to_user: str,
    currency: str,
    amount: str,
    fee_amount: str,
    description: str
) -> str:
    transfer = Transfer(
        created_at=datetime_from_timestamp(get_timestamp()),
        task_id=str(uuid.uuid4()),
        from_user=User.objects.get(uuid=from_user),
        to_user=User.objects.get(uuid=to_user),
        currency=currency,
        amount=amount,
        fee_amount=fee_amount,
        description=description,
    )
    CurrentTransfer(task_id=transfer.task_id).save()
    sended = Producer.send_kafka_message(
        topic=settings.KAFKA_NOTBANK_SYNC_TOPIC,
        message=transfer.to_sync_task_trama())
    if not sended:
        raise NotBankKafkaException(
            "failed to send to notbank-sync kafka topic")

    sended = Producer.send_kafka_message(
        topic=settings.KAFKA_BALANCE_MANAGER_TASK_TOPIC,
        message=transfer.to_balance_manager_task_trama()
    )
    if not sended:
        raise NotBankKafkaException(
            "failed to send to balance-manager-task kafka topic")
    return transfer.task_id


def get_conversion(
    from_user_uuid: str,
    from_asset: str,
    from_amount: str,
    to_asset: str,
    fee_amount: str
) -> str:
    trama_data = NanoBancoQuote(
        timestamp=get_timestamp(),
        django_user_ID=from_user_uuid,
        from_currency=from_asset,
        to_currency=to_asset,
        from_amount=from_amount,
        request_id=str(uuid.uuid4()),
        fee_amount=fee_amount,
    )
    sended = Producer.send_kafka_message(
        topic=settings.KAFKA_QUOTE_SERVICE_NANOBANCO_QUOTE,
        message=trama_data.to_trama())
    if not sended:
        raise NotBankKafkaException(
            "failed to send to TODO:SOME-TOPIC kafka topic")  # TODO: not use some topic


def execute_conversion(*, user_uuid: str, request_id: str, fee_amount: str, description: str):
    try:
        CurrentConversion(request_id=request_id).save()
    except IntegrityError:
        raise ConversionAlreadyRunningException()
    try:
        quote: Quote = Quote.objects.get(request_id=request_id)
        # TODO: should be deleted in all instances (in a task after sync)
    except Quote.DoesNotExist:
        raise QuoteNotFoundException()
    try:
        user = User.objects.get(uuid=user_uuid)
    except User.DoesNotExist:
        raise UserNotFoundException()
    conversion = Conversion(
        task_id=uuid.uuid4(),
        user=user,
        from_currency=quote.from_currency,
        from_amount=quote.from_amount,
        to_currency=quote.to_currency,
        fee_amount=Decimal(fee_amount),
        description=description,
    )
    sended = Producer.send_kafka_message(
        topic=settings.KAFKA_NOTBANK_SYNC_TOPIC,
        message=conversion.to_sync_task_trama())
    if not sended:
        raise NotBankKafkaException(
            "failed to send to notbank-sync kafka topic")
    sended = Producer.send_kafka_message(
        topic=settings.KAFKA_BALANCE_MANAGER_TASK_TOPIC,
        message=conversion.to_balance_manager_task_trama())
    if not sended:
        raise NotBankKafkaException(
            "failed to send to balance-manager-task kafka topic")
    return conversion.task_id



def deposit(*, user_uuid: str, request_id: str, currency: str, amount: str,  fee: str):
    try:
        CurrentDeposit(request_id=request_id).save()
    except IntegrityError:
        raise DepositAlreadyRunningException()
    try:
        quote: Quote = Quote.objects.get(request_id=request_id)
        # TODO: should be deleted in all instances (in a task after sync)
    except Quote.DoesNotExist:
        raise QuoteNotFoundException()
    try:
        user = User.objects.get(uuid=user_uuid)
    except User.DoesNotExist:
        raise UserNotFoundException()
    conversion = Conversion(
        task_id=uuid.uuid4(),
        user=user,
        from_currency=quote.from_currency,
        from_amount=quote.from_amount,
        to_currency=quote.to_currency,
        fee_amount=Decimal(fee),
    )
    sended = Producer.send_kafka_message(
        topic=settings.KAFKA_NOTBANK_SYNC_TOPIC,
        message=conversion.to_sync_task_trama())
    if not sended:
        raise NotBankKafkaException(
            "failed to send to notbank-sync kafka topic")
        
    sended = Producer.send_kafka_message(
        topic=settings.KAFKA_BALANCE_MANAGER_TASK_TOPIC,
        message=conversion.to_balance_manager_task_trama())
    if not sended:
        raise NotBankKafkaException(
            "failed to send to balance-manager-task kafka topic")
    return conversion.task_id


def get_quote(*, request_id: str) -> Optional[Quote]:
    try:
        return Quote.objects.get(request_id=request_id)
    except Quote.DoesNotExist:
        return None


def get_current_conversions(*, status: str, creation_date: str) -> List[CurrentConversion]:
    if status:
        return list(CurrentConversion.objects.filter(active=status).order_by('-created_at'))
    if creation_date:
        return list(CurrentConversion.objects.filter(created_at=creation_date).order_by('-created_at'))


def get_transfer_request_list_of_user(*, user_uuid: str) -> List[TransferRequest]:
    return list(TransferRequest.objects.filter(transaction__to_user__user_uuid=user_uuid))


def get_transfer_of_user(*, user_uuid: str) -> List[Transfer]:
    return list(Transfer.objects.filter(from_user__uuid=user_uuid))


def get_all_transfers(*, status: str, creation_date: str) -> List[Transfer]:
    if status:
        return list(Transfer.objects.filter(status=status).order_by('-amount'))
    if creation_date:
        return list(Transfer.objects.filter(created_at=creation_date).order_by('-amount'))


def sync_transfer_request(
    transfer_request: TransferRequest
) -> None:
    sended = Producer.send_kafka_message(
        topic=settings.KAFKA_NOTBANK_SYNC_TOPIC,
        message=transfer_request.to_sync_task_trama())
    if not sended:
        raise NotBankKafkaException(
            "failed to send to notbank internal kafka topic")
    return


def sync_new_transfer_request(
    from_user_uuid: str,
    to_user_uuid: str,
    currency: str,
    amount: str,
    fee_amount: str,
    description: str,
) -> None:
    transfer_request = TransferRequest(
        transfer=Transfer(
            task_id=uuid.uuid4(),
            from_user=User.objects.get(uuid=from_user_uuid),
            to_user=User.objects.get(uuid=to_user_uuid),
            currency=currency,
            amount=Decimal(amount),
            fee_amount=Decimal(fee_amount),
            description=description,
        ),
        status=TransferRequest.STATUS.PENDING,
    )
    sync_transfer_request(transfer_request)


def accept_or_reject_transfer_request(task_id: str, accept: bool):
    try:
        transfer_request: TransferRequest = TransferRequest.objects.get(
            task_id=task_id
        )
    except TransferRequest.DoesNotExist:
        raise TransferRequestNotFoundException()

    if transfer_request.status != transfer_request.STATUS.PENDING:
        raise TransferRequestAlreadyCommitedException()
    if accept:
        # we only send to balance manager when the transfer is accepted
        # timestamp here is the time of the transaction (now)
        # not the time of the creation of the transfer (transfer.created_at)
        transfer: Transfer = transfer_request.transfer
        balance_manager_task = transfer.to_balance_manager_task()
        balance_manager_task.timestamp = get_timestamp()
        sended = Producer.send_kafka_message(
            topic=settings.KAFKA_BALANCE_MANAGER_TASK_TOPIC,
            message=balance_manager_task.to_trama(),
        )
        if not sended:
            raise NotBankKafkaException(
                'failed to send kafka message to balance manager task topic')
    # we always propagate
    new_status = {
        True: TransferRequest.STATUS.ACCEPTED,
        False: TransferRequest.STATUS.REJECTED,
    }
    transfer_request.status = new_status[accept]
    sync_transfer_request(transfer_request)
