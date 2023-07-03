import unittest
from notbank.base.utils.kafka.authentication import sign
from notbank.base.utils.kafka.tramas.balance_manager_task import BalanceManagerTask
from notbank.base.utils.kafka.tramas.exceptions import TramaFormatException, TramaValidationException


class BalanceManagerTaskTestCase(unittest.TestCase):
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
        self.timestamp = "1652981386000".rjust(13, ' ')
        self.task_id = "f636cfc7-c937-4e73-91cb-8e49fd7179ef".rjust(36, ' ')
        self.task_name = BalanceManagerTask.TASK_NAME.CONVERSION.value.rjust(16)
        self.from_user_uuid = "1e9bb042-6789-4183-8587-4d40ab130b85".rjust(
            36, ' ')
        self.from_currency = "CRO".rjust(8, ' ')
        self.from_amount = "1652981386.833999".rjust(37, ' ')
        self.to_user_uuid = "a29bbq42-6782-4183-8587-4d40ab188b34".rjust(
            36, ' ')
        self.to_currency = "btc".rjust(8, ' ')
        self.to_amount = "3262256.6732524".rjust(37, ' ')
        self.fee_amount = "1652981656.679874".rjust(37, ' ')
        self.task_detail = "detalle del task a salvarse, son 64 caracteres asi que estamos".rjust(
            64, ' ')
        self.trama_data: str = ''.join([
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

    def test_read_from_trama(self):
        trama = self.trama_data + sign(self.trama_data)
        task = BalanceManagerTask.from_trama(trama)
        self.assertEqual(self.timestamp.lstrip(), task.timestamp)
        self.assertEqual(self.task_id.lstrip(), task.task_id)
        self.assertEqual(self.task_name.lstrip(), task.task_name.value)
        self.assertEqual(
            self.from_user_uuid.lstrip(),
            task.from_user_uuid
        )
        self.assertEqual(
            self.from_currency.lstrip(),
            task.from_currency
        )
        self.assertEqual(
            self.from_amount.lstrip(),
            task.from_amount
        )
        self.assertEqual(
            self.to_user_uuid.lstrip(),
            task.to_user_uuid
        )
        self.assertEqual(self.to_currency.lstrip(), task.to_currency)
        self.assertEqual(
            self.to_amount.lstrip(),
            task.to_amount
        )
        self.assertEqual(self.fee_amount.lstrip(), task.fee_amount)
        self.assertEqual(self.task_detail.lstrip(), task.task_detail)

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
            TramaFormatException,
            BalanceManagerTask.from_trama,
            trama,
        )

    def test_read_from_badly_signed_trama(self):
        # ! corrupting signature
        trama = self.trama_data + sign(self.trama_data)[:-1] + 'l'
        self.assertRaises(
            TramaValidationException,
            BalanceManagerTask.from_trama,
            trama,
        )


if __name__ == '__main__':
    unittest.main()
