from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _
from notbank.base.models.base import CommonModel
from notbank.base.utils.kafka.tramas.balance_manager_task import \
    BalanceManagerTask
from notbank.base.utils.kafka.tramas.nanobanco_quote import NanoBancoQuote
from notbank.base.utils.kafka.tramas.sync_task import SyncTask
from notbank.base.utils.time import (datetime_from_timestamp, get_timestamp,
                                     str_timestamp_from_datetime)
from notbank.transactions.models.user import User


class Conversion(CommonModel):
    task_id = models.UUIDField(editable=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    from_currency = models.CharField(max_length=8)
    from_amount = models.DecimalField(max_digits=36, decimal_places=18)
    to_currency = models.CharField(max_length=8)
    to_amount = models.DecimalField(max_digits=36, decimal_places=18)
    fee_amount = models.DecimalField(max_digits=36, decimal_places=18)
    description = models.CharField(max_length=256, null=True, blank=True)

    class STATUS(models.IntegerChoices):
        BM_PENDING = 0, _("Esperando a balance manager")
        BM_ERROR = 1, _("Error en balance manager")
        BM_SUCCESS_QS_PENDING = 2, _(
            "Éxito en balance manager, esperando quote service"
        )
        QS_ERROR_NOT_ENOUGH_BALANCE = 3, _("Error en quote service, balance insuficiente")
        QS_ERROR_NOT_POSSIBLE_TO_COMPLY =4, ("Error en quote service, imposible cumplir")
        QS_SUCCESS = 5, _("Éxito en quote service")

    status = models.IntegerField(
        choices=STATUS.choices, default=STATUS.BM_PENDING)

    def to_nanobanco_quote(self) -> NanoBancoQuote:
        return NanoBancoQuote(
            timestamp=get_timestamp(),
            django_user_ID=str(self.user.uuid),
            from_currency=self.from_currency,
            to_currency=self.to_currency,
            from_amount=str(self.from_amount),
            request_id=str(self.task_id),
            fee_amount=str(self.fee_amount),
        )

    def to_nanobanco_quote_trama(self, sign: bool = True) -> str:
        return self.to_nanobanco_quote().to_trama(sign)

    def to_balance_manager_task(self) -> BalanceManagerTask:
        return BalanceManagerTask(
            timestamp=str_timestamp_from_datetime(self.created_at),
            task_id=str(self.task_id),
            task_name=BalanceManagerTask.TASK_NAME.CONVERSION,
            from_user_uuid=str(self.user.uuid),
            from_currency=self.from_currency,
            from_amount=str(self.from_amount),
            to_currency=self.to_currency,
            to_amount=str(self.to_amount),
            fee_amount=str(self.fee_amount),
        )

    def to_balance_manager_task_trama(self, sign: bool = True) -> str:
        return self.to_balance_manager_task().to_trama(sign)

    def to_sync_task(self) -> SyncTask:
        return SyncTask(
            timestamp=str_timestamp_from_datetime(self.created_at),
            task_name=SyncTask.TASK_NAME.CONVERSION,
            task_id=str(self.task_id),
            from_user_uuid=str(self.user.uuid),
            from_currency=self.from_currency,
            from_amount=str(self.from_amount),
            to_currency=self.to_currency,
            to_amount=str(self.to_amount),
            fee_amount=str(self.fee_amount),
            description=self.description if self.description else '',
        )

    def to_sync_task_trama(self, sign: bool = True) -> str:
        return self.to_sync_task().to_trama(sign)

    @classmethod
    def from_sync_task_trama(cls, trama: str, with_signature: bool = True):
        sync_task = SyncTask.from_trama(trama, with_signature)
        conversion = cls(
            created_at=datetime_from_timestamp(sync_task.timestamp),
            task_id=sync_task.task_id,
            user=User.objects.get(uuid=sync_task.from_user_uuid),
            from_currency=sync_task.from_currency,
            from_amount=Decimal(sync_task.from_amount),
            to_currency=sync_task.to_currency,
            to_amount=Decimal(sync_task.to_amount),
            fee_amount=Decimal(sync_task.fee_amount),
        )
        if sync_task.description != '':
            conversion.description = sync_task.description,
        return conversion
