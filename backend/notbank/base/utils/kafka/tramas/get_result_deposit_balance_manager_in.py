from dataclasses import dataclass
from enum import Enum
import json
from typing import List, Any

from notbank.base.utils.kafka.tramas.trama_reader import TramaReader
from notbank.base.utils.kafka.tramas.trama_writer import TramaWriter


# get result deposit input msg kafka
@dataclass
class GetResultDepositBalanceManagerIn:
    timestamp: str  # 13
    taskName: str
    task_id: str
    status: str
    

    @classmethod
    def from_trama(cls, trama: str, with_signature: bool = True):
        trama_reader = TramaReader(trama, with_signature)
        timestamp = trama_reader.read(13)
        taskName = trama_reader.read(16)
        task_id = trama_reader.read(36)
        status = trama_reader.read(7)


        return cls(timestamp = timestamp, taskName=taskName, task_id = task_id, status = status)