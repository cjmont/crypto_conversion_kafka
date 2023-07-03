
from django.db import models
from django.utils.translation import gettext_lazy as _
from notbank.base.models.base import CommonModel
from notbank.base.utils.kafka.tramas.sync_task import SyncTask
from notbank.base.utils.time import datetime_from_timestamp
from notbank.transactions.models import Transfer


class TransferRequest(CommonModel):
    task_id = models.UUIDField(editable=False)
    transfer = models.OneToOneField(
        Transfer,
        on_delete=models.PROTECT
    )

    class STATUS(models.IntegerChoices):
        PENDING = 0, _("Pendiente")
        ACCEPTED = 1, _("Éxito")
        REJECTED = 2, _("Error")

    status = models.IntegerField(choices=STATUS.choices)

    def to_sync_task(self) -> SyncTask:
        task = self.transfer.to_sync_task()
        task.task_name = SyncTask.TASK_NAME.TRANSFER_REQUEST
        task.status = str(self.status.value)
        return task

    def to_sync_task_trama(self, sign: bool = True) -> str:
        return self.to_sync_task().to_trama(sign)

    @classmethod
    def from_sync_task(cls, task: SyncTask):
        return cls(
            created_at=datetime_from_timestamp(task.timestamp),
            task_id=task.task_id,
            transfer=Transfer.from_sync_task(task),
            status=cls.STATUS(int(task.status)),
        )

    @classmethod
    def from_sync_task_trama(cls, trama: str, with_signature: bool = True):
        task = SyncTask.from_trama(trama, with_signature)
        return cls.from_sync_task(task)
