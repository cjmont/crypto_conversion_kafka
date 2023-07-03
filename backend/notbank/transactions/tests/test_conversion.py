from decimal import Decimal
from uuid import uuid4

from django.test import TestCase
from notbank.base.utils.kafka.tramas.balance_manager_task import BalanceManagerTask
from notbank.base.utils.kafka.tramas.sync_task import SyncTask
from notbank.base.utils.time import datetime_from_timestamp, get_timestamp, str_timestamp_from_datetime
from notbank.transactions.models import (Conversion, User)


class SaveTransferTaskTest(TestCase):
    def setUp(self):
        self.user = User(uuid=uuid4())
        self.user.save()

        self.conversion = Conversion(
            created_at=datetime_from_timestamp(get_timestamp()),
            task_id=str(uuid4()),
            user=self.user,
            from_currency='EOS',
            from_amount=Decimal('564.36'),
            to_currency='ETH',
            to_amount=Decimal('54.6'),
            fee_amount=Decimal('4'),
        )

    def tearDown(self) -> None:
        self.user.delete()

    def test_sync_task__task_name(self):
        trama = self.conversion.to_sync_task_trama()
        sync_task = SyncTask.from_trama(trama)
        self.assertEqual(sync_task.task_name, SyncTask.TASK_NAME.CONVERSION)

    def test_pass_via_sync_task_trama(self):
        trama = self.conversion.to_sync_task_trama()
        new_conversion = Conversion.from_sync_task_trama(trama)
        self.assertEqual(self.conversion.created_at, new_conversion.created_at)
        self.assertEqual(self.conversion.task_id, new_conversion.task_id)
        self.assertEqual(self.conversion.user, new_conversion.user)
        self.assertEqual(self.conversion.from_currency,
                         new_conversion.from_currency)
        self.assertEqual(self.conversion.from_amount,
                         new_conversion.from_amount)
        self.assertEqual(self.conversion.to_currency,
                         new_conversion.to_currency)
        self.assertEqual(self.conversion.to_amount, new_conversion.to_amount)
        self.assertEqual(self.conversion.fee_amount, new_conversion.fee_amount)

    def test_convert_to_balance_manager_task(self):
        balance_manager_task = self.conversion.to_balance_manager_task()
        self.assertEqual(str_timestamp_from_datetime(
            self.conversion.created_at), balance_manager_task.timestamp)
        self.assertEqual(self.conversion.task_id, balance_manager_task.task_id)
        self.assertEqual(BalanceManagerTask.TASK_NAME.CONVERSION,
                         balance_manager_task.task_name)
        self.assertEqual(str(self.conversion.user.uuid),
                         balance_manager_task.from_user_uuid)
        self.assertEqual(self.conversion.from_currency,
                         balance_manager_task.from_currency)
        self.assertEqual(str(self.conversion.from_amount),
                         balance_manager_task.from_amount)
        self.assertEqual(self.conversion.to_currency,
                         balance_manager_task.to_currency)
        self.assertEqual(str(self.conversion.to_amount),
                         balance_manager_task.to_amount)
        self.assertEqual(str(self.conversion.fee_amount),
                         balance_manager_task.fee_amount)

    def test_convert_to_nanobanco_quote(self):
        nanobanco_quote = self.conversion.to_nanobanco_quote()
        self.assertEqual(str(self.conversion.user.uuid),
                         nanobanco_quote.django_user_ID)
        self.assertEqual(self.conversion.from_currency,
                         nanobanco_quote.from_currency)
        self.assertEqual(self.conversion.to_currency,
                         nanobanco_quote.to_currency)
        self.assertEqual(str(self.conversion.from_amount),
                         nanobanco_quote.from_amount)
        self.assertEqual(self.conversion.task_id, nanobanco_quote.request_id)
        self.assertEqual(str(self.conversion.fee_amount),
                         nanobanco_quote.fee_amount)
