
from dataclasses import dataclass
from enum import Enum

from notbank.base.utils.kafka.tramas.exceptions import TramaFormatException
from notbank.base.utils.kafka.tramas.trama_reader import TramaReader
from notbank.base.utils.kafka.tramas.trama_writer import TramaWriter

# input to the balance manager


@dataclass
class BalanceManagerTask:
    timestamp: str  # 13
    task_id: str  # 36

    class TASK_NAME(Enum):
        CONVERSION = 'conversion'
        TRANSFER = 'transfer'
    task_name: TASK_NAME  # str  # 16

    from_user_uuid: str = ''  # 36
    from_currency: str = ''  # 8
    from_amount: str = ''  # 37

    to_user_uuid: str = ''  # 36
    to_currency: str = ''  # 8
    to_amount: str = ''  # 37

    fee_amount: str = ''  # 37
    task_detail: str = ''  # 64

    def to_trama(self, sign: bool = True) -> str:
        return TramaWriter.write([
            (self.timestamp, 13),
            (self.task_id, 36),
            (self.task_name.value, 16),

            (self.from_user_uuid, 36),
            (self.from_currency, 8),
            (self.from_amount, 37),

            (self.to_user_uuid, 36),
            (self.to_currency, 8),
            (self.to_amount, 37),

            (self.fee_amount, 37),
            (self.task_detail, 64),
        ], sign)

    @classmethod
    def from_trama(cls, trama: str, with_signature: bool = True):
        trama_reader = TramaReader(trama, with_signature)
        try:
          balance_manager_task = cls(
              timestamp=trama_reader.read(13),
              task_id=trama_reader.read(36),
              task_name=cls.TASK_NAME(trama_reader.read(16)),

              from_user_uuid=trama_reader.read(36),
              from_currency=trama_reader.read(8),
              from_amount=trama_reader.read(37),

              to_user_uuid=trama_reader.read(36),
              to_currency=trama_reader.read(8),
              to_amount=trama_reader.read(37),

              fee_amount=trama_reader.read(37),
              task_detail=trama_reader.read(64),
          )
        except Exception as e:
            raise TramaFormatException(e)
        if not trama_reader.is_done():
            raise TramaFormatException('unread chars left')
        return balance_manager_task
