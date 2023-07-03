
from dataclasses import dataclass
from typing import Optional

from notbank.base.utils.kafka.tramas.exceptions import TramaFormatException
from notbank.base.utils.kafka.tramas.trama_reader import TramaReader
from notbank.base.utils.kafka.tramas.trama_writer import TramaWriter


@dataclass
class UserData:
    timestamp: str  # 13
    uuid: str  # 36
    phone: str  # 32
    firebase_token: Optional[str]  # 255, optional

    def to_trama(self, sign: bool = True):
        return TramaWriter.write([
            (self.timestamp, 13),
            (self.uuid, 36),
            (self.phone, 32),
            (self.firebase_token, 255),
        ], sign)

    @classmethod
    def from_trama(cls, trama: str, with_signature: bool = True):
        trama_reader = TramaReader(trama, with_signature)
        user_data = cls(
            timestamp=trama_reader.read(13),
            uuid=trama_reader.read(36),
            phone=trama_reader.read(32),
            firebase_token=trama_reader.read(255)
        )
        if not trama_reader.is_done():
            raise TramaFormatException('unread chars left')
        return user_data
