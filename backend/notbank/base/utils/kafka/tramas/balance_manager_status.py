

# balance manager status output

import json
from ast import Dict
from dataclasses import dataclass
from enum import Enum
from notbank.base.utils.kafka.tramas.exceptions import TramaFormatException

from notbank.base.utils.kafka.tramas.trama_reader import TramaReader


@dataclass
class BalanceManagerStatus:
    timestamp: str  # 13
    task_id: str  # from json

    class STATUS(Enum):
        SUCCESS = "success"
        ERROR = "error"
    status: STATUS  # from json

    @classmethod
    def from_trama(cls, trama: str, with_signature: bool = True):
        trama_reader = TramaReader(trama, with_signature)
        timestamp = trama_reader.read(13)
        data: Dict[str, str] = json.loads(trama_reader.get_unread())
        try:
            task_id = data['taskId']
        except KeyError:
            raise TramaFormatException(f'json key taskId not present')
        try:
            status = cls.STATUS(data['status'])
        except KeyError:
            raise TramaFormatException(f'json key status not present')
        return cls(
            timestamp=timestamp,
            task_id=task_id,
            status=status,
        )
