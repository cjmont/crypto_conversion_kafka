from decimal import Decimal
from uuid import uuid4

from django.test import TestCase
from notbank.base.models.base import Log
from notbank.base.utils.kafka.tramas.sync_task import SyncTask
from notbank.base.utils.time import datetime_from_timestamp, get_timestamp
from notbank.tasks.tasks.save_transfer import save_transfer
from notbank.transactions.models import (BMStatusWaitingSyncTask, Transfer,
                                         User)

SECONDS = 1


class SaveTransferTaskTest(TestCase):
    def setUp(self):
        self.uuid_user_1 = uuid4()
        self.uuid_user_2 = uuid4()

        User(uuid=self.uuid_user_1).save()
        User(uuid=self.uuid_user_2).save()

        self.task_id = uuid4()
        self.timestamp = get_timestamp()
        self.currency = 'CRO'
        self.amount = '123123.12'
        self.fee_amount = '10'

        self.sync_task = SyncTask(
            timestamp=self.timestamp,
            task_name=SyncTask.TASK_NAME.TRANSFER,
            task_id=str(self.task_id),
            from_user_uuid=str(self.uuid_user_1),
            from_currency=self.currency,
            from_amount=self.amount,
            to_user_uuid=str(self.uuid_user_2),
            fee_amount=self.fee_amount,
        )

    def tearDown(self) -> None:
        try:
            Transfer.objects.get(task_id=self.task_id).delete()
        except Transfer.DoesNotExist:
            pass
        User.objects.get(uuid=self.uuid_user_1).delete()
        User.objects.get(uuid=self.uuid_user_2).delete()

    def test_propagate_transfer(self):
        save_transfer(self.sync_task.to_trama())
        try:
            transfer = Transfer.objects.get(task_id=self.task_id)
            self.assertEqual(
                transfer.created_at,
                datetime_from_timestamp(self.timestamp)
            )
            self.assertEqual(transfer.from_user.uuid, self.uuid_user_1)
            self.assertEqual(transfer.to_user.uuid, self.uuid_user_2)
            self.assertEqual(transfer.currency, self.currency)
            self.assertEqual(transfer.amount, Decimal(self.amount))
            self.assertEqual(transfer.fee_amount, Decimal(self.fee_amount))
        except Transfer.DoesNotExist:
            self.fail('transfer not saved')

    def test_unsigned_trama(self):
        save_transfer(self.sync_task.to_trama(sign=False))
        try:
            Transfer.objects.get(task_id=self.task_id)
            self.fail()
        except Transfer.DoesNotExist:
            self.assertGreaterEqual(len(Log.objects.all()), 1)

    def test_invalid_user(self):
        self.sync_task.from_user_uuid = str(uuid4())
        save_transfer(self.sync_task.to_trama())
        try:
            Transfer.objects.get(task_id=self.sync_task.task_id)
            self.fail()
        except Transfer.DoesNotExist:
            pass

    def test_with_pending_status(self):
        BMStatusWaitingSyncTask(
            task_id=self.task_id,
            status=BMStatusWaitingSyncTask.STATUS.ERROR
        ).save()
        save_transfer(self.sync_task.to_trama())
        transfer = Transfer.objects.get(task_id=self.task_id)
        self.assertEqual(transfer.status, Transfer.STATUS.ERROR)
        try:
            BMStatusWaitingSyncTask.objects.get(task_id=self.task_id)
            self.fail()
        except BMStatusWaitingSyncTask.DoesNotExist:
            pass
