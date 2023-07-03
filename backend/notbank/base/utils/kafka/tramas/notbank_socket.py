from dataclasses import dataclass
import json
from typing import Dict

from notbank.base.utils.kafka.tramas.trama_writer import TramaWriter


@dataclass
class NotbankSocket:
    timestamp: str  # 13
    user_uuid: str  # 36
    event_name: str  # 16
    data: Dict[str, any]

    def to_trama(self, sign: bool = True) -> str:
        json_str = json.dumps(self.data)
        return TramaWriter.write([
            (self.timestamp, 13),
            (self.user_uuid, 36),
            (self.event_name, 16),
            (json_str, len(json_str)),
        ], sign)
