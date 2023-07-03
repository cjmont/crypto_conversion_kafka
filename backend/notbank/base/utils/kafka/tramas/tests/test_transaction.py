from unittest import TestCase
import unittest
from notbank.base.utils.kafka.authentication import sign
from notbank.base.utils.kafka.tramas.balance_manager_transaction import BalanceManagerTransaction


class BalanceManagerTransactionTestCase(TestCase):
    trama_data: str
    timestamp: str
    task_name: str
    task_id: str
    task_detail: str
    user_uuid: str
    currency: str
    operation_amount: str
    balance: str
    executed_at: str
    partition: str
    offset: str

    def setUp(self) -> None:
        self.timestamp = "1652981386000".rjust(13, ' ')
        self.task_name = "save_transaction".rjust(16, ' ')
        self.task_id = "f636cfc7-c937-4e73-91cb-8e49fd7179ef".rjust(36, ' ')
        self.task_detail = "detalle del task a salvarse, son 64 caracteres asi que estamos".rjust(
            64, ' ')
        self.user_uuid = "1e9bb042-6789-4183-8587-4d40ab130b85".rjust(36, ' ')
        self.currency = "CRO".rjust(8, ' ')
        self.operation_amount = "1652981386.833999".rjust(37, ' ')
        self.balance = "1652981656.679874".rjust(37, ' ')
        self.executed_at = "1234567890123".rjust(19, ' ')
        self.partition = "13".rjust(13, ' ')
        self.offset = "10".rjust(13, ' ')

        self.trama_data = ''.join([
            self.timestamp,
            self.task_name,
            self.task_id,
            self.task_detail,
            self.user_uuid,
            self.currency,
            self.operation_amount,
            self.balance,
            self.executed_at,
            self.partition,
            self.offset
        ])

    def test_read_from_trama(self):
        trama = self.trama_data + sign(self.trama_data)
        transaction = BalanceManagerTransaction.from_trama(trama)

        self.assertEqual(self.timestamp.lstrip(), transaction.timestamp)
        self.assertEqual(self.task_name.lstrip(), transaction.task_name)
        self.assertEqual(self.task_id.lstrip(), transaction.task_id)
        self.assertEqual(self.task_detail.lstrip(), transaction.task_detail)
        self.assertEqual(self.user_uuid.lstrip(), transaction.user_uuid)
        self.assertEqual(
            self.operation_amount.lstrip(),
            transaction.operation_amount,
        )
        self.assertEqual(self.balance.lstrip(), transaction.balance)
        self.assertEqual(self.executed_at.lstrip(), transaction.executed_at)
        self.assertEqual(self.partition.lstrip(), transaction.partition)
        self.assertEqual(self.offset.lstrip(), transaction.offset)

    def test_read_from_invalid_trama(self):
        # ! less than 37 characters => fails
        operation_amount = "                1652981386.833999"
        trama_data = ''.join([
            self.timestamp,
            self.task_name,
            self.task_id,
            self.task_detail,
            self.user_uuid,
            self.currency,
            operation_amount,
            self.balance,
            self.executed_at,
            self.partition,
            self.offset
        ])
        trama = trama_data + sign(trama_data)
        self.assertRaises(
            Exception,
            BalanceManagerTransaction.from_trama,
            trama,
        )

    def test_read_from_badly_signed_trama(self):
        # ! corrupting signature
        trama = self.trama_data + sign(self.trama_data)[:-1] + 'l'
        self.assertRaises(
            Exception,
            BalanceManagerTransaction.from_trama,
            trama,
        )


if __name__ == '__main__':
    unittest.main()
