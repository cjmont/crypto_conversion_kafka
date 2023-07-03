from dataclasses import dataclass

from notbank.base.utils.kafka.tramas.exceptions import TramaFormatException
from notbank.base.utils.kafka.tramas.trama_writer import TramaWriter
from notbank.base.utils.kafka.tramas.trama_reader import TramaReader


@dataclass
class QuoteListener:
    timestamp: str
    from_currency: str
    to_currency: str
    from_amount: str
    to_amount: str
    request_id: str
    perfect_amount: str

    def to_trama(self, sign: bool = True) -> str:
        return TramaWriter.write([
            (self.timestamp, 13),
            (self.from_currency, 8),
            (self.to_currency, 8),
            (self.from_amount, 37),
            (self.to_amount, 37),
            (self.request_id, 36),
            (self.perfect_amount, 37),
        ], sign)


    @classmethod
    def from_trama(cls, trama: str, with_signature: bool = True):
        trama_reader = TramaReader(trama, with_signature)
        quote_listener = cls(
            timestamp=trama_reader.read(13),
            #task_id=trama_reader.read(36),
            #task_name=trama_reader.read(16),

            from_currency=trama_reader.read(8),
            to_currency=trama_reader.read(8),
            from_amount=trama_reader.read(37),

            to_amount=trama_reader.read(37),
            request_id=trama_reader.read(36),
            perfect_amount=trama_reader.read(37),
        )
        if not trama_reader.is_done():
            raise TramaFormatException('unread chars left')
        return quote_listener
