from decimal import Decimal
from unittest import mock
from unittest.mock import ANY, patch
from uuid import uuid4
from django.conf import settings

from django.test import TestCase
from notbank.base.utils.kafka.producer import Producer
from notbank.base.utils.kafka.tramas.sync_task import SyncTask
from notbank.base.utils.time import datetime_from_timestamp, get_timestamp
from notbank.tasks.tasks.save_conversion import save_conversion
from notbank.transactions.models import (Conversion, BMStatusWaitingSyncTask,
                                         User)
from notbank.transactions.models.current_conversion import CurrentConversion

SECONDS = 1


class SaveTransferTaskTest(TestCase):
    def setUp(self):
        self.user_1 = User(uuid=uuid4())
        self.user_2 = User(uuid=uuid4())
        self.user_1.save()
        self.user_2.save()

        self.sync_task = SyncTask(
            timestamp=get_timestamp(),
            task_name=SyncTask.TASK_NAME.TRANSFER,
            task_id=str(uuid4()),
            from_user_uuid=str(self.user_1.uuid),
            from_currency='ADA',
            from_amount='7554.23',
            to_currency='BTC',
            to_amount='44.4',
            fee_amount='35',
        )

    def tearDown(self) -> None:
        try:
            Conversion.objects.get(task_id=self.sync_task.task_id).delete()
        except Conversion.DoesNotExist:
            pass
        self.user_1.delete()
        self.user_2.delete()

    def test_sync_conversion(self):
        save_conversion(self.sync_task.to_trama())
        try:
            conversion = Conversion.objects.get(task_id=self.sync_task.task_id)
            self.assertEqual(
                conversion.created_at,
                datetime_from_timestamp(self.sync_task.timestamp),
            )
            self.assertEqual(conversion.user.uuid, self.user_1.uuid)
            self.assertEqual(conversion.from_currency,
                             self.sync_task.from_currency)
            self.assertEqual(conversion.from_amount,
                             Decimal(self.sync_task.from_amount))
            self.assertEqual(conversion.to_currency,
                             self.sync_task.to_currency)
            self.assertEqual(conversion.to_amount,
                             Decimal(self.sync_task.to_amount))
            self.assertEqual(conversion.fee_amount,
                             Decimal(self.sync_task.fee_amount))
        except Conversion.DoesNotExist:
            self.fail('conversion not saved')

    def test_invalid_trama(self):
        self.sync_task.task_id = str(uuid4())
        save_conversion(self.sync_task.to_trama())
        try:
            Conversion.objects.get(task_id=self.sync_task.task_id)
            self.fail()
        except Conversion.DoesNotExist:
            pass

    def test_invalid_user(self):
        self.sync_task.from_user_uuid = str(uuid4())
        save_conversion(self.sync_task.to_trama())
        try:
            Conversion.objects.get(task_id=self.sync_task.task_id)
            self.fail()
        except Conversion.DoesNotExist:
            pass

    def test_with_pending_status(self):
        BMStatusWaitingSyncTask(
            task_id=self.sync_task.task_id,
            status=BMStatusWaitingSyncTask.STATUS.ERROR
        ).save()
        save_conversion(self.sync_task.to_trama())
        conversion = Conversion.objects.get(task_id=self.sync_task.task_id)
        self.assertEqual(conversion.status, Conversion.STATUS.BM_ERROR)
        try:
            BMStatusWaitingSyncTask.objects.get(task_id=self.sync_task.task_id)
            self.fail()
        except BMStatusWaitingSyncTask.DoesNotExist:
            pass

    @patch.object(Producer, 'send_kafka_message')
    def test_with_pending_conversion_send_to_quote_service(self, mock_send_kafka_message):
        BMStatusWaitingSyncTask(
            task_id=self.sync_task.task_id,
            status=BMStatusWaitingSyncTask.STATUS.SUCCESS
        ).save()
        CurrentConversion(request_id=self.sync_task.task_id).save()
        save_conversion(self.sync_task.to_trama())
        mock_send_kafka_message.assert_any_call(
            topic=settings.KAFKA_QUOTE_SERVICE_TOPIC,
            message=ANY,
        )

    @patch.object(Producer, 'send_kafka_message')
    def test_with_no_pending_conversion_no_send_to_quote_service(self, mock_send_kafka_message):
        BMStatusWaitingSyncTask(
            task_id=self.sync_task.task_id,
            status=BMStatusWaitingSyncTask.STATUS.SUCCESS
        ).save()
        save_conversion(self.sync_task.to_trama())
        mock_send_kafka_message.assert_not_called()
