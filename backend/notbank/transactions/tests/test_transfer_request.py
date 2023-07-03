
from decimal import Decimal
import unittest
import uuid
from notbank.base.utils.kafka.tramas.sync_task import SyncTask
from notbank.base.utils.time import datetime_from_timestamp, get_timestamp

from notbank.transactions.models import Transfer
from notbank.transactions.models.transfer_request import TransferRequest
from notbank.transactions.models.user import User


class TransferRequestViaTrama(unittest.TestCase):
    def setUp(self) -> None:
        self.from_user = User(uuid=uuid.uuid4())
        self.to_user = User(uuid=uuid.uuid4())
        task_id = str(uuid.uuid4())
        self.transfer = Transfer(
            created_at=datetime_from_timestamp(get_timestamp()),
            task_id=task_id,
            from_user=self.from_user,
            to_user=self.to_user,
            currency='ADA',
            amount=Decimal('222.22'),
            fee_amount=Decimal('4'),
            status=Transfer.STATUS.PENDING,
        )
        self.transfer_request = TransferRequest(
            created_at=self.transfer.created_at,
            transfer=self.transfer,
            task_id=task_id,
            status=TransferRequest.STATUS.PENDING,
        )
        self.from_user.save()
        self.to_user.save()

    def tearDown(self) -> None:
        self.to_user.delete()
        self.from_user.delete()

    def test_sync_task__task_name(self):
        trama = self.transfer_request.to_sync_task_trama()
        sync_task = SyncTask.from_trama(trama)
        self.assertEqual(sync_task.task_name,
                         SyncTask.TASK_NAME.TRANSFER_REQUEST)

    def test_pass_via_sync_task(self):
        trama = self.transfer_request.to_sync_task_trama()
        new_transfer_request = TransferRequest.from_sync_task_trama(trama)
        self.assertEqual(self.transfer_request.created_at,
                         new_transfer_request.created_at)
        self.assertEqual(self.transfer_request.task_id,
                         new_transfer_request.task_id)
        self.assertEqual(self.transfer_request.status,
                         new_transfer_request.status)

        self.assertEqual(self.transfer_request.transfer.created_at,
                         new_transfer_request.transfer.created_at)
        self.assertEqual(self.transfer_request.transfer.task_id,
                         new_transfer_request.transfer.task_id)
        self.assertEqual(self.transfer_request.transfer.from_user,
                         new_transfer_request.transfer.from_user)
        self.assertEqual(self.transfer_request.transfer.to_user,
                         new_transfer_request.transfer.to_user)
        self.assertEqual(self.transfer_request.transfer.currency,
                         new_transfer_request.transfer.currency)
        self.assertEqual(self.transfer_request.transfer.amount,
                         new_transfer_request.transfer.amount)
        self.assertEqual(self.transfer_request.transfer.fee_amount,
                         new_transfer_request.transfer.fee_amount)
        self.assertEqual(self.transfer_request.transfer.status,
                         new_transfer_request.transfer.status)
