
import unittest
import uuid
from decimal import Decimal
from unittest.mock import ANY, patch

from django.conf import settings
from notbank.base.exceptions import (QuoteNotFoundException,
                                     UserNotFoundException)
from notbank.base.utils.kafka.producer import Producer
from notbank.transactions.models import CurrentConversion, Quote, User
from notbank.transactions.services import (execute_conversion, get_conversion,
                                           new_transfer)


@patch.object(Producer, 'send_kafka_message')
class ServicesTestCase(unittest.TestCase):
    def setUp(self):
        self.user = User(uuid=uuid.uuid4())
        self.user.save()
        self.user_2 = User(uuid=uuid.uuid4())
        self.user_2.save()

    def tearDown(self) -> None:
        Quote.objects.all().delete()
        CurrentConversion.objects.all().delete()
        # Conversion.objects.all().delete()
        User.objects.all().delete()

    def test_execute_conversion(self, mock_send_kafka_message):
        request_id = uuid.uuid4()
        quote = Quote(
            request_id=request_id,
            from_currency='CRO',
            to_currency='USD',
            from_amount=Decimal('39'),
            to_amount=Decimal('3'),
            perfect_amount=Decimal('3'),
        )
        quote.save()
        execute_conversion(
            user_uuid=str(self.user.uuid),
            request_id=request_id,
            fee_amount='22',
            description='',
        )

        mock_send_kafka_message.assert_any_call(
            topic=settings.KAFKA_NOTBANK_SYNC_TOPIC,
            message=ANY)
        mock_send_kafka_message.assert_any_call(
            topic=settings.KAFKA_BALANCE_MANAGER_TASK_TOPIC,
            message=ANY)
        quote.delete()

    def test_execute_conversion_no_user_exception(self, mock_send_kafka_message):
        request_id = uuid.uuid4()
        exe_conversion = Quote(
            request_id=request_id,
            from_currency='CRO',
            to_currency='USD',
            from_amount=Decimal('39'),
            to_amount=Decimal('3'),
            perfect_amount=Decimal('3'),
        )
        exe_conversion.save()

        self.assertRaises(
            UserNotFoundException,
            execute_conversion,
            user_uuid=uuid.uuid4(),
            request_id=request_id,
            fee_amount='22',
            description='',
        )

    def test_execute_conversion_no_quote(self, mock_send_kafka_message):
        self.assertRaises(
            QuoteNotFoundException,
            execute_conversion,
            user_uuid=uuid.uuid4(),
            request_id=uuid.uuid4(),
            fee_amount='22',
            description='',
        )

    def test_new_transfer(self, mock_send_kafka_message):
        new_transfer(
            from_user=str(self.user.uuid),
            to_user=str(self.user_2.uuid),
            currency='CRO',
            amount='12.121212',
            fee_amount='3',
            description='',
        )

        mock_send_kafka_message.assert_any_call(
            topic=settings.KAFKA_NOTBANK_SYNC_TOPIC,
            message=ANY)
        mock_send_kafka_message.assert_any_call(
            topic=settings.KAFKA_BALANCE_MANAGER_TASK_TOPIC,
            message=ANY)

    def test_get_conversion(self, mock_send_kafka_message):
        get_conversion(
            from_user_uuid=str(self.user.uuid),
            from_asset='BTC',
            from_amount='1222',
            to_asset='CRO',
            fee_amount='44',
        )
        mock_send_kafka_message.assert_any_call(
            topic=settings.KAFKA_QUOTE_SERVICE_NANOBANCO_QUOTE,
            message=ANY,
        )
