
from dataclasses import dataclass
from enum import Enum
from notbank.base.utils.kafka.tramas.exceptions import TramaFormatException
from notbank.base.utils.kafka.tramas.trama_reader import TramaReader
from notbank.base.utils.kafka.tramas.trama_writer import TramaWriter
from notbank.base.utils.time import get_timestamp
from django.conf import settings
# balance manager transaction output
@dataclass
class NotifyDeposit:
    timestamp: str  # 13
    task_id: str  # 36
    status: str  # 1
    

    def to_trama(task_id, status, sign: bool = True) -> str:
        return TramaWriter.write([
            (get_timestamp(), 13),
            (task_id, 36),
            (status, 8),
        ], sign)