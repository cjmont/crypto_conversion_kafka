import json
import unittest
from notbank.base.utils.kafka.tramas.payment_listener_notify_transactions import PaymentListenerNotifyTransactions
from notbank.base.utils.kafka.authentication import sign
from notbank.base.utils.kafka.tramas.balance_manager_task import BalanceManagerTask
from notbank.base.utils.kafka.tramas.balance_manager_status import BalanceManagerStatus
from notbank.base.utils.kafka.tramas.exceptions import TramaFormatException, TramaValidationException


class PaymentListenerNotifyTransactionsTestCase(unittest.TestCase):
    trama_data: str
    timestamp: int  # 13
    task_id: str  # vairable
    status: str  # variable
    data: str  # dict with taskId and status

    def setUp(self) -> None:
        self.timestamp = "1652981386000".rjust(13, ' ')
        self.userId = "583e87c9-871a-404d-810d-3aa124661e65".rjust(36, ' ')
        self.task = "payment_transaction"
        self.transactions = [{
                                "id": 36896428,
                                "created_at": "2020-11-12T10:27:26.135Z",
                                "updated_at": "2020-11-12T10:42:29.065Z",
                                "status": "SUCCESS",
                                "type": "DEPOSIT",
                                "subtype": "BLOCKCHAIN",
                                "native": {
                                        "tx_id": "a271ad64-5f34-4115-a63e-1cb5bbe4f67e",
                                        "index": 429625504,
                                        "currency": "BTC",
                                        "amount": "0.04836614",
                                        "hash": "4d7ae7c9d6fe84405ae167b3f0beacx8c68eb5a9d5189bckeb65d5e306427oe6",
                                        "address": "3E8WKmTJzaTsBc4kvuEJVjPNtak6vQRcRv",
                                        "confirmations": 9999,
                                        "senders": [
                                        "0xd959463c3fcb0d2124bb7ac642d6a6573a6c5aba"
                                    ]
                            }},
                             {
                                "id": 36896429,
                                "created_at": "2020-11-12T10:27:26.135Z",
                                "updated_at": "2020-11-12T10:42:29.065Z",
                                "status": "SUCCESS",
                                "type": "DEPOSIT2",
                                "subtype": "BLOCKCHAIN",
                                "native": {
                                        "tx_id": "a271ad64-5f34-4115-a63e-1cb5bbe4f67e",
                                        "index": 429625504,
                                        "currency": "BTC",
                                        "amount": "6.64836614",
                                        "hash": "4d7ae7c9d6fe84405ae167b3f0beacx8c68eb5a9d5189bckeb65d5e306427oe6",
                                        "address": "3E8WKmTJzaTsBc4kvuEJVjPNtak6vQRcRv",
                                        "confirmations": 33333,
                                        "senders": [
                                        "0xd959463c3fcb0d2124bb7ac642d6a6573a6c5aba"
                                    ]
                            }},
                             {
                                "id": 36896429,
                                "created_at": "2020-11-12T10:27:26.135Z",
                                "updated_at": "2020-11-12T10:42:29.065Z",
                                "status": "SUCCESS",
                                "type": "DEPOSIT3",
                                "subtype": "BLOCKCHAIN",
                                "native": {
                                        "tx_id": "a271ad64-5f34-4115-a63e-1cb5bbe4f67e",
                                        "index": 429625504,
                                        "currency": "BTC",
                                        "amount": "7.64836614",
                                        "hash": "4d7ae7c9d6fe84405ae167b3f0beacx8c68eb5a9d5189bckeb65d5e306427oe6",
                                        "address": "3E8WKmTJzaTsBc4kvuEJVjPNtak6vQRcRv",
                                        "confirmations": 1111,
                                        "senders": [
                                        "0xd959463c3fcb0d2124bb7ac642d6a6573a6c5aba"
                                    ]
                            }}]
        self.data = {
            "transactions": self.transactions,
            "userId": self.userId,
        }
        self.trama_data: str = ''.join([
            self.timestamp,
            json.dumps({'task': self.task, 'data': self.data})
        ])

   

    def test_read_from_badly_signed_trama(self):
        # ! corrupting signature
        trama = self.trama_data + sign(self.trama_data)#[:-1] #+ 'l'
        data = PaymentListenerNotifyTransactions.from_trama(trama)
        print(trama)
        self.assertEqual(data.timestamp, self.timestamp)
        self.assertEqual(data.userId, self.userId)
        self.assertEqual(data.task.value, self.task)
        self.assertEqual(data.transactions, self.transactions)
        

if __name__ == '__main__':
    unittest.main()
