from decimal import Decimal
import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from notbank.base.models.base import CommonModel
from notbank.base.utils.kafka.tramas.balance_manager_task import \
    BalanceManagerTask
from notbank.base.utils.kafka.tramas.sync_task import SyncTask
from notbank.base.utils.time import (datetime_from_timestamp,
                                     str_timestamp_from_datetime)
from notbank.transactions.models.user import User


class Transfer(CommonModel):
    from_user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="from_user"
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="to_user"
    )
    task_id = models.UUIDField(editable=False)
    currency = models.CharField(max_length=8)
    amount = models.DecimalField(max_digits=36, decimal_places=18)
    fee_amount = models.DecimalField(max_digits=36, decimal_places=18)
    description = models.CharField(max_length=256, null=True, blank=True)

    class STATUS(models.IntegerChoices):
        PENDING = 0, _("Éxito")
        SUCCESS = 1, _("Error")
        ERROR = 2, _("Pendiente")

    status = models.IntegerField(
        choices=STATUS.choices, default=STATUS.PENDING)

    def to_balance_manager_task(self) -> BalanceManagerTask:
        """When converted to a balance manager task, it looses its description
        """
        return BalanceManagerTask(
            timestamp=str_timestamp_from_datetime(self.created_at),
            task_id=str(self.task_id),
            task_name=BalanceManagerTask.TASK_NAME.TRANSFER,
            from_user_uuid=str(self.from_user.uuid),
            from_currency=self.currency,
            from_amount=str(self.amount),
            to_user_uuid=str(self.to_user.uuid),
            fee_amount=str(self.fee_amount),
        )

    def to_sync_task(self) -> SyncTask:
        return SyncTask(
            timestamp=str_timestamp_from_datetime(self.created_at),
            task_name=SyncTask.TASK_NAME.TRANSFER,
            task_id=str(self.task_id),
            from_user_uuid=str(self.from_user.uuid),
            from_currency=self.currency,
            from_amount=str(self.amount),
            to_user_uuid=str(self.to_user.uuid),
            fee_amount=str(self.fee_amount),
            description=self.description if self.description else '',
        )

    def to_balance_manager_task_trama(self, sign: bool = True) -> str:
        """uses balance manager task trama (no description), used in the balance manager.
        """
        return self.to_balance_manager_task().to_trama(sign)

    def to_sync_task_trama(self, sign: bool = True) -> str:
        """ uses sync task trama, used for synchronization between service instances
        """
        return self.to_sync_task().to_trama(sign)

    @classmethod
    def from_sync_task(cls, task: SyncTask):
        from_user = User.objects.get(uuid=task.from_user_uuid)
        to_user = User.objects.get(uuid=task.to_user_uuid)
        return cls(
            created_at=datetime_from_timestamp(task.timestamp),
            task_id=task.task_id,
            from_user=from_user,
            to_user=to_user,
            currency=task.from_currency,
            amount=Decimal(task.from_amount),
            fee_amount=Decimal(task.fee_amount),
            description=task.description,
        )

    @classmethod
    def from_sync_task_trama(cls, trama: str, with_signature: bool = True):
        task = SyncTask.from_trama(trama, with_signature)
        return cls.from_sync_task(task)

    @classmethod
    def from_balance_manager_task(cls, task: BalanceManagerTask):
        from_user = User.objects.get(uuid=task.from_user_uuid)
        to_user = User.objects.get(uuid=task.to_user_uuid)
        return cls(
            created_at=datetime_from_timestamp(task.timestamp),
            task_id=task.task_id,
            from_user=from_user,
            to_user=to_user,
            currency=task.from_currency,
            amount=Decimal(task.from_amount),
            fee_amount=Decimal(task.fee_amount),
        )

    @classmethod
    def from_balance_manager_task_trama(cls, trama: str, with_signature: bool = True):
        task = BalanceManagerTask.from_trama(trama, with_signature)
        return cls.from_balance_manager_task(task)
