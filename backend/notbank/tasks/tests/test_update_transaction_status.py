from decimal import Decimal
import json
from unittest.mock import ANY, patch
from urllib import request
from uuid import uuid4
from django.conf import settings

from django.test import TestCase
from notbank.base.utils.kafka.producer import Producer
from notbank.base.utils.kafka.authentication import sign
from notbank.base.utils.kafka.tramas.balance_manager_status import BalanceManagerStatus
from notbank.base.utils.time import get_timestamp
from notbank.tasks.tasks.update_transaction_status import update_transaction_status
from notbank.transactions.models import (Conversion, BMStatusWaitingSyncTask, Transfer,
                                         User)
from notbank.transactions.models.current_conversion import CurrentConversion

SECONDS = 1


class SaveTransferTaskTest(TestCase):
    def setUp(self):
        self.user_1 = User(uuid=uuid4())
        self.user_2 = User(uuid=uuid4())
        self.user_1.save()
        self.user_2.save()

        self.conversion_task_id = uuid4()
        self.conversion = Conversion(
            user=self.user_1,
            from_currency='CRO',
            to_currency='BTC',
            from_amount=Decimal('1231.11'),
            to_amount=Decimal('5'),
            fee_amount=Decimal('10.2'),
            description='some description',
            task_id=str(self.conversion_task_id),
            status=Conversion.STATUS.BM_PENDING,
        )
        CurrentConversion(request_id=self.conversion.task_id).save()
        self.conversion.save()

        self.transfer_task_id = uuid4()
        self.transfer = Transfer(
            from_user=self.user_1,
            to_user=self.user_2,
            task_id=self.transfer_task_id,
            currency='CRO',
            amount=Decimal('12221.1'),
            fee_amount=Decimal('2'),
            description='some description',
            status=Transfer.STATUS.PENDING,
        )
        self.transfer.save()

    def tearDown(self) -> None:
        CurrentConversion.objects.all().delete()
        try:
            self.conversion.delete()
        except Exception as e:
            pass
        try:
            self.transfer.delete()
        except Exception as e:
            pass
        self.user_1.delete()
        self.user_2.delete()

    def test_update_transfer_status(self):
        timestamp = get_timestamp()
        js = {
            'taskId': str(self.transfer_task_id),
            'status': BalanceManagerStatus.STATUS.ERROR.value,
        }
        js_str = json.dumps(js)
        trama_data = timestamp + js_str
        trama = trama_data + sign(trama_data)

        update_transaction_status(trama)

        transfer = Transfer.objects.get(task_id=self.transfer_task_id)
        self.assertEqual(transfer.status, Transfer.STATUS.ERROR)
        self.assertEqual(len(BMStatusWaitingSyncTask.objects.all()), 0)

    @patch.object(Producer, 'send_kafka_message')
    def test_update_conversion_status_result_success(self, mock_send_kafka_message):
        BMStatusWaitingSyncTask.objects.all().delete()
        BMStatusWaitingSyncTask(task_id=self.conversion_task_id,
                                status=BMStatusWaitingSyncTask.STATUS.PENDING).save()
        timestamp = get_timestamp()
        js = {
            'taskId': str(self.conversion_task_id),
            'status': BalanceManagerStatus.STATUS.SUCCESS.value,
        }
        js_str = json.dumps(js)
        trama_data = timestamp + js_str
        trama = trama_data + sign(trama_data)

        update_transaction_status(trama)

        conversion = Conversion.objects.get(task_id=self.conversion_task_id)
        self.assertEqual(conversion.status,
                         Conversion.STATUS.BM_SUCCESS_QS_PENDING)
        self.assertEqual(len(BMStatusWaitingSyncTask.objects.all()), 1)
        mock_send_kafka_message.assert_any_call(
            topic=settings.KAFKA_QUOTE_SERVICE_TOPIC,
            message=ANY,
        )

    @patch.object(Producer, 'send_kafka_message')
    def test_update_conversion_status_result_error(self, mock_send_kafka_message):
        BMStatusWaitingSyncTask.objects.all().delete()
        BMStatusWaitingSyncTask(task_id=self.conversion_task_id,
                                status=BMStatusWaitingSyncTask.STATUS.PENDING).save()
        timestamp = get_timestamp()
        js = {
            'taskId': str(self.conversion_task_id),
            'status': BalanceManagerStatus.STATUS.ERROR.value,
        }
        js_str = json.dumps(js)
        trama_data = timestamp + js_str
        trama = trama_data + sign(trama_data)

        update_transaction_status(trama)

        conversion = Conversion.objects.get(task_id=self.conversion_task_id)
        self.assertEqual(conversion.status, Conversion.STATUS.BM_ERROR)
        self.assertEqual(len(BMStatusWaitingSyncTask.objects.all()), 1)
        mock_send_kafka_message.assert_not_called()
