import json
import unittest
from notbank.base.utils.kafka.tramas import get_fee_return_cryptomarket_in
from notbank.base.utils.kafka.tramas.get_fee_return_cryptomarket_in import GetFeeReturnCryptoMarketIn
from notbank.base.utils.kafka.authentication import sign
from notbank.base.utils.kafka.tramas.trama_reader import TramaReader


class ReturnFeeTestCase(unittest.TestCase):
    trama_data: str
    timestamp: int  # 13
    task_id: str  # vairable
    status: str  # variable
    data: str  # dict with taskId and status

    def setUp(self) -> None:
        self.timestamp = "1652981386000".rjust(13, ' ')
        self.task = "return_fee"
        self.request_id = "777f1418-73f2-43ec-ab92-c7d36da28132".rjust(36, ' ')
        self.fee = "0.01"
        self.data = {
            "request_id": self.request_id,
            "fee": self.fee,
        }
        self.trama_data: str = ''.join([
            self.timestamp,
            json.dumps({'task': self.task, 'data': self.data})
        ])

   

    def test_read_from_badly_signed_trama(self):
        # ! corrupting signature
        trama = self.trama_data + sign(self.trama_data)#[:-1] #+ 'l'
        data = GetFeeReturnCryptoMarketIn.from_trama(trama)
        print(trama)
        self.assertEqual(data.timestamp, self.timestamp)
        self.assertEqual(data.task, self.task)
        self.assertEqual(data.request_id, self.request_id)
        self.assertEqual(data.fee, self.fee)
        

if __name__ == '__main__':
    unittest.main()
