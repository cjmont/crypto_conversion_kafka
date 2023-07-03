import json
import unittest
from notbank.base.utils.kafka.authentication import sign
from notbank.base.utils.kafka.tramas.balance_manager_task import BalanceManagerTask
from notbank.base.utils.kafka.tramas.balance_manager_status import BalanceManagerStatus
from notbank.base.utils.kafka.tramas.exceptions import TramaFormatException, TramaValidationException


class BalanceManagerTransferStatusTestCase(unittest.TestCase):
    trama_data: str
    timestamp: int  # 13
    task_id: str  # vairable
    status: str  # variable
    data: str  # dict with taskId and status

    def setUp(self) -> None:
        self.timestamp = "1652981386000".rjust(13, ' ')
        self.task_id = "f636cfc7-c937-4e73-91cb-8e49fd7179ef".rjust(36, ' ')
        self.status = "error"
        self.data = {
            "taskId": self.task_id,
            "status": self.status,
        }
        self.trama_data: str = ''.join([
            self.timestamp,
            json.dumps(self.data)
        ])

    def test_read_from_trama(self):
        trama = self.trama_data + sign(self.trama_data)
        transfer_status = BalanceManagerStatus.from_trama(trama)
        self.assertEqual(self.timestamp.lstrip(), transfer_status.timestamp)
        self.assertEqual(self.task_id, transfer_status.task_id)
        self.assertEqual(
            transfer_status.status,
            BalanceManagerStatus.STATUS.ERROR
        )

    def test_read_status_success(self):
        trama_data = ''.join([
            self.timestamp,
            json.dumps({
                "taskId": self.task_id,
                "status": "success",
            })
        ])
        trama = trama_data + sign(trama_data)
        transfer_status = BalanceManagerStatus.from_trama(trama)
        self.assertEqual(
            transfer_status.status,
            BalanceManagerStatus.STATUS.SUCCESS
        )

    def test_read_from_invalid_trama(self):
        trama_data = ''.join([
            self.timestamp,
            json.dumps({
                # ! not known keyword => fails
                "task007": self.task_id,
                "status": self.status,
            })
        ])
        trama = trama_data + sign(trama_data)
        self.assertRaises(
            TramaFormatException,
            BalanceManagerStatus.from_trama,
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
