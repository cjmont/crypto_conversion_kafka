
from dataclasses import dataclass
from enum import Enum
from notbank.base.utils.kafka.tramas.exceptions import TramaFormatException
from notbank.base.utils.kafka.tramas.trama_reader import TramaReader
from notbank.base.utils.kafka.tramas.trama_writer import TramaWriter
from notbank.base.utils.time import get_timestamp
from django.conf import settings
# balance manager transaction output
@dataclass
class DepositTransaction:
    timestamp: str  # 13
    
    class TASK_NAME(Enum):
        GET_FEE = 'deposit'

    task_name: TASK_NAME  # 16

    def to_trama(user_uuid, currency, amount, fee, sign: bool = True) -> str:
        return TramaWriter.write([
            (get_timestamp(), 13),
            (settings.DEPOSIT, 16),
            (user_uuid, 36),
            (currency, 8),
            (amount, 37),
            (fee, 37),
        ], sign)