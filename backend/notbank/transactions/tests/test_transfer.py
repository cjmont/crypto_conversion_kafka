from datetime import datetime
from decimal import Decimal
import unittest
from notbank.base.utils.kafka.authentication import sign
from notbank.base.utils.kafka.tramas.balance_manager_task import BalanceManagerTask
from notbank.base.utils.time import datetime_from_timestamp, get_timestamp, str_timestamp_from_datetime
from notbank.transactions.models import Transfer, User


class TransferViaTrama(unittest.TestCase):
    trama_data: str
    timestamp: int  # 13
    task_id: str  # 36
    task_name: str  # 16
    from_user_uuid: str  # 36
    from_currency: str  # 8
    from_amount: str  # 37
    to_user_uuid: str  # 36
    to_currency: str  # 8
    to_amount: str  # 37
    fee_amount: str  # 37
    task_detail: str  # 64

    def setUp(self) -> None:
        for transfer in Transfer.objects.all():
            transfer.delete()
        for user in User.objects.all():
            user.delete()
        self.timestamp = f'{get_timestamp()}'.rjust(13)
        self.task_id = "f636cfc7-c937-4e73-91cb-8e49fd7179ef".rjust(36)
        self.task_name = "transfer".rjust(16)
        self.from_user_uuid = "22b8f3de-b310-460a-ac9d-2068a6a78a15".rjust(36)
        self.from_currency = "CRO".rjust(8)
        self.from_amount = "1652981386.833999".rjust(37)
        self.to_user_uuid = "2dff5a12-81ab-4f3d-9e89-8046135e71b3".rjust(36)
        self.to_currency = "".rjust(8)
        self.to_amount = "".rjust(37)
        self.fee_amount = "1652981656.679874".rjust(37)
        self.task_detail = "".rjust(64)
        self.description = "a short description of a transfer of assets"
        self.trama_data = ''.join([
            self.timestamp,
            self.task_id,
            self.task_name,
            self.from_user_uuid,
            self.from_currency,
            self.from_amount,
            self.to_user_uuid,
            self.to_currency,
            self.to_amount,
            self.fee_amount,
            self.task_detail,
        ])
        self.from_user = User(uuid=self.from_user_uuid)
        self.from_user.save()
        self.to_user = User(uuid=self.to_user_uuid)
        self.to_user.save()
        self.transfer = Transfer(
            created_at=datetime_from_timestamp(self.timestamp),
            task_id=self.task_id,
            from_user=self.from_user,
            to_user=self.to_user,
            currency='CRO',
            amount=Decimal('123.22'),
            fee_amount=Decimal('10'),
            description='description of a transfer',
            status=Transfer.STATUS.PENDING,
        )
        self.transfer.save()

    def tearDown(self) -> None:
        self.transfer.delete()
        self.from_user.delete()
        self.to_user.delete()

    def test_read_from_trama(self):
        trama = self.trama_data + sign(self.trama_data)
        transfer = Transfer.from_balance_manager_task_trama(trama)

        self.assertEqual(
            self.timestamp.lstrip(),
            str_timestamp_from_datetime(transfer.created_at)
        )
        self.assertEqual(self.task_id.lstrip(), transfer.task_id)
        self.assertEqual(self.from_user_uuid.lstrip(),
                         str(transfer.from_user.uuid))
        self.assertEqual(self.to_user_uuid.lstrip(),
                         str(transfer.to_user.uuid))
        self.assertEqual(self.from_currency.lstrip(), transfer.currency)
        self.assertEqual(self.from_amount.lstrip(), str(transfer.amount))
        self.assertEqual(self.fee_amount.lstrip(), str(transfer.fee_amount))

    def test_read_from_invalid_trama(self):
        # ! less than 37 characters => fails
        from_amount = "1652981386.833999".rjust(30, ' ')
        trama_data = ''.join([
            self.timestamp,
            self.task_id,
            self.task_name,
            self.from_user_uuid,
            self.from_currency,
            from_amount,
            self.to_user_uuid,
            self.to_amount,
            self.fee_amount,
            self.task_detail,
        ])
        trama = trama_data + sign(trama_data)
        self.assertRaises(
            Exception,
            Transfer.from_balance_manager_task_trama,
            trama
        )

    def test_read_from_badly_signed_trama(self):
        # ! corrupting signature
        trama = self.trama_data + sign(self.trama_data)[:-1] + 'l'
        self.assertRaises(
            Exception,
            Transfer.from_balance_manager_task_trama,
            trama,
        )

    def test_write_to_trama(self):
        trama = self.trama_data + sign(self.trama_data)
        transfer = Transfer.from_balance_manager_task_trama(trama)
        self.assertEqual(
            self.trama_data, transfer.to_balance_manager_task_trama(sign=False))
        self.assertEqual(trama, transfer.to_balance_manager_task_trama())

    def test_pass_via_sync_task_trama(self):
        trama = self.transfer.to_sync_task_trama()
        new_transfer = Transfer.from_sync_task_trama(trama)
        self.assertEqual(self.transfer.created_at, new_transfer.created_at)
        self.assertEqual(self.transfer.task_id, new_transfer.task_id)
        self.assertEqual(self.transfer.from_user, new_transfer.from_user)
        self.assertEqual(self.transfer.to_user, new_transfer.to_user)
        self.assertEqual(self.transfer.currency, new_transfer.currency)
        self.assertEqual(self.transfer.amount, new_transfer.amount)
        self.assertEqual(self.transfer.fee_amount, new_transfer.fee_amount)
        self.assertEqual(self.transfer.description, new_transfer.description)
        self.assertEqual(self.transfer.status, new_transfer.status)

    def test_convert_to_balance_manager_task(self):
        balance_manager_task = self.transfer.to_balance_manager_task()
        self.assertEqual(str_timestamp_from_datetime(self.transfer.created_at),
                         balance_manager_task.timestamp)
        self.assertEqual(self.transfer.task_id, balance_manager_task.task_id)
        self.assertEqual(str(self.transfer.from_user.uuid),
                         balance_manager_task.from_user_uuid)
        self.assertEqual(str(self.transfer.to_user.uuid),
                         balance_manager_task.to_user_uuid)
        self.assertEqual(self.transfer.currency,
                         balance_manager_task.from_currency)
        self.assertEqual(str(self.transfer.amount),
                         balance_manager_task.from_amount)
        self.assertEqual(str(self.transfer.fee_amount),
                         balance_manager_task.fee_amount)
        self.assertEqual(balance_manager_task.task_name,
                         BalanceManagerTask.TASK_NAME.TRANSFER)
        self.assertEqual(balance_manager_task.to_currency, '')
        self.assertEqual(balance_manager_task.to_amount, '')
        self.assertEqual(balance_manager_task.task_detail, '')


if __name__ == '__main__':
    unittest.main()
