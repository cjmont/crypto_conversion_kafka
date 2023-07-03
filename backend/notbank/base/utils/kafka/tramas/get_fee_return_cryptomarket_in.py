from dataclasses import dataclass
from enum import Enum
import json
from typing import List, Any

from notbank.base.utils.kafka.tramas.trama_reader import TramaReader
from notbank.base.utils.kafka.tramas.trama_writer import TramaWriter


# Payment get fee input msg kafka
@dataclass
class GetFeeReturnCryptoMarketIn:
    timestamp: str  # 13

    class TASK_NAME(Enum):
        PAYMENT_TRANSACTIONS = 'return_fee'
    task: TASK_NAME
    request_id: str
    fee: str

    #transactions: List[Any]


    @classmethod
    def from_trama(cls, trama: str, with_signature: bool = True):
        trama_reader = TramaReader(trama, with_signature)
        timestamp = trama_reader.read(13)
        js = trama_reader.get_unread()
        data_ = json.loads(js)
        task = cls.TASK_NAME(data_['task'])
        data = data_['data']


        return cls(timestamp = timestamp, task = task.value, request_id = data['request_id'], fee = data['fee'])