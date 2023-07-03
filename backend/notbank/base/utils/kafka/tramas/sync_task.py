from dataclasses import dataclass
from enum import Enum, IntFlag
import json
from typing import Dict

from notbank.base.utils.kafka.tramas.exceptions import TramaFormatException
from notbank.base.utils.kafka.tramas.trama_reader import TramaReader
from notbank.base.utils.kafka.tramas.trama_writer import TramaWriter


TRANSACTION = 'transaction'
TASK = 'task'
META = 'meta'
DATA = 'data'


@dataclass
class SyncTask:
    timestamp: str  # 13

    class Transaction(Enum):
        TRANSFER = 'TRANSFER'
        CONVERSION = 'CONVERSION'
    transaction: Transaction  # 16

    class Task(Enum):
        SYNC_UNCOMMITED = 'sync-uncommited'
        SYNC_COMMITED = 'sync-commited'
    task: Task

    data: Dict[str, str]

    def to_trama(self, sign: bool = True) -> str:
        json_dict = {
            DATA: self.data,
            META: {
                TRANSACTION: self.transaction.value,
                TASK: self.task.value
            },
        }
        json_str = json.dumps(json_dict)
        return TramaWriter.write([
            (self.timestamp, 13),
            (json_str, len(json_str)),
        ], sign)

    @classmethod
    def from_trama(cls, trama: str, with_signature: bool = True):
        trama_reader = TramaReader(trama, with_signature)
        timestamp = trama_reader.read(13)
        data_ = json.loads(trama_reader.get_unread())
        internal_task = cls(
            timestamp=timestamp,
            transaction=cls.Transaction(data_[META][TRANSACTION]),
            task=cls.Task(data_[META][TASK]),
            data=data_[DATA]
        )
        return internal_task
