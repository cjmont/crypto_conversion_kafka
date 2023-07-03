from dataclasses import dataclass
from notbank.base.utils.kafka.tramas.exceptions import TramaFormatException
from notbank.base.utils.kafka.tramas.trama_reader import TramaReader

from notbank.base.utils.kafka.tramas.trama_writer import TramaWriter


@dataclass
class NanoBancoQuote:
    timestamp: str
    django_user_ID: str
    from_currency: str
    to_currency: str
    from_amount: str
    request_id: str
    fee_amount: str

    def to_trama(self, sign: bool = True) -> str:
        return TramaWriter.write([
            (self.timestamp, 13),
            (self.django_user_ID, 36),
            (self.from_currency, 8),
            (self.to_currency, 8),
            (self.from_amount, 37),
            (self.request_id, 36),
            (self.fee_amount, 37),
        ], sign)

    @classmethod
    def from_trama(cls, trama: str, with_signature: bool = True):
        trama_reader = TramaReader(trama, with_signature)
        nanobanco_quote = cls(
            timestamp=trama_reader.read(13),
            django_user_ID=trama_reader.read(36),
            from_currency=trama_reader.read(8),
            to_currency=trama_reader.read(8),
            from_amount=trama_reader.read(37),
            request_id=trama_reader.read(36),
            fee_amount=trama_reader.read(37),
        )
        if not trama_reader.is_done():
            raise TramaFormatException('unread chars left')
        return nanobanco_quote
