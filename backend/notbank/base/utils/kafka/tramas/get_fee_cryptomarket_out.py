
from dataclasses import dataclass
from enum import Enum
import json
import uuid

from notbank.base.utils.kafka.tramas.trama_reader import TramaReader
from notbank.base.utils.kafka.tramas.trama_writer import TramaWriter
from notbank.base.utils.time import get_timestamp
from django.conf import settings

# get fee from cryptomarket output msg kafka
@dataclass
class GetFeeCryptoMarketOut:
    timestamp: str  # 13

    class TASK_NAME(Enum):
        GET_FEE = 'get_fee'
    task: TASK_NAME
    user_id: str

    
    def uuid_generate():
        return str(uuid.uuid4())

    def to_trama(currency, amount, sign: bool = True) -> str:
        js = {
            'task': settings.GET_FEE,
            'data': {
                'request_id': str(uuid.uuid4()),
                'currency': currency,
                'amount': amount,
            }
        }
        js_str = json.dumps(js)
        return TramaWriter.write([
            (get_timestamp(), 13),
            (js_str, len(js_str)),
        ], sign)
        
        