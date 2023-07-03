import json
import unittest
from notbank.base.utils.kafka.tramas.get_result_deposit_balance_manager_in import GetResultDepositBalanceManagerIn
from notbank.base.utils.kafka.authentication import sign
from notbank.base.utils.kafka.tramas.trama_reader import TramaReader


class ReturnResultDepositTestCase(unittest.TestCase):
    trama_data: str
    timestamp: int  # 13
    task_id: str  # vairable
    estado: str  # variable
 
    

    def setUp(self) -> None:
        self.timestamp = "1652981386000".rjust(13, ' ')
        self.taskName = "deposit".rjust(16, ' ')
        self.task_id = "d5692a67-bbc5-4815-9879-94b99b7c14d8".rjust(36, ' ')
        self.status = "success".rjust(7, ' ')
        self.trama_data: str = ''.join([
            self.timestamp,
            self.taskName,
            self.task_id,
            self.status,
        ])
   

    def test_read_from_badly_signed_trama(self):
        # ! corrupting signature     
        trama = self.trama_data + sign(self.trama_data)#[:-1] #+ 'l'      
        data = GetResultDepositBalanceManagerIn.from_trama(trama , True)   
        print(trama)
        self.assertEqual(data.timestamp, self.timestamp)
        self.assertEqual(data.taskName, self.taskName)
        self.assertEqual(data.task_id, self.task_id)
        self.assertEqual(data.status, self.status)
        
        

if __name__ == '__main__':
    unittest.main()