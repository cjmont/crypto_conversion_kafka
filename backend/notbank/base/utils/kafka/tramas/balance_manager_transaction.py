
from dataclasses import dataclass

from notbank.base.utils.kafka.tramas.exceptions import TramaFormatException
from notbank.base.utils.kafka.tramas.trama_reader import TramaReader
from notbank.base.utils.kafka.tramas.trama_writer import TramaWriter


# balance manager transaction output
@dataclass
class BalanceManagerTransaction:
    timestamp: str  # 13
    task_name: str  # 16
    task_id: str  # 36
    task_detail: str  # 64
    user_uuid: str  # 36
    currency: str  # 8
    operation_amount: str  # 37
    balance: str  # 37
    executed_at: str  # 19 (datetime) (DD/MM/YYYY)
    partition: str  # 13
    offset: str  # 13

    def to_trama(self, sign: bool = True) -> str:
        return TramaWriter.write([
            (self.timestamp, 13),
            (self.task_name, 16),
            (self.task_id, 36),
            (self.task_detail, 64),
            (self.user_uuid, 36),
            (self.currency, 8),
            (self.operation_amount, 37),
            (self.balance, 37),
            (self.executed_at, 19),
            (self.partition, 13),
            (self.offset, 13),
        ], sign)

    @classmethod
    def from_trama(cls, trama: str, with_signature: bool = True):
        trama_reader = TramaReader(trama, with_signature)
        balance_manager_transaction = cls(
            timestamp=trama_reader.read(13),
            task_name=trama_reader.read(16),
            task_id=trama_reader.read(36),
            task_detail=trama_reader.read(64),
            user_uuid=trama_reader.read(36),
            currency=trama_reader.read(8),
            operation_amount=trama_reader.read(37),
            balance=trama_reader.read(37),
            executed_at=trama_reader.read(19),
            partition=trama_reader.read(13),
            offset=trama_reader.read(13),
        )
        if not trama_reader.is_done():
            raise TramaFormatException('unread chars left')
        return balance_manager_transaction
