from dataclasses import dataclass

from notbank.base.utils.kafka.tramas.trama_writer import TramaWriter


@dataclass
class QuoteServiceInternalExecuteIn:
    timestamp: str
    request_id: str

    def to_trama(self, sign: bool = True) -> str:
        return TramaWriter.write([
            (self.timestamp, 13),
            (self.request_id, 36),
        ], sign)
