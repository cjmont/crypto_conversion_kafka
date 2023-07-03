
from dataclasses import dataclass
from enum import Enum
import json

from notbank.base.utils.kafka.tramas.trama_reader import TramaReader
from notbank.base.utils.kafka.tramas.trama_writer import TramaWriter


# balance manager transaction output
@dataclass
class QuoteServiceInternalExecuteOut:
    timestamp: str  # 13

    class TASK_NAME(Enum):
        EXECUTE_QUOTE = 'execute_quote'
    task: TASK_NAME
    request_id: str

    class STATE(Enum):
        EXECUTED = 'executed'
        NOT_ENOUGH_BALANCE = 'not_enough_balance'
        NOT_POSSIBLE_TO_COMPLY = 'not_possible_to_comply'
    state: STATE

    currency_in_name: str
    currency_in_amount: str
    currency_out_name: str
    currency_out_amount: str
    error: str = ''

    def to_trama(self, sign: bool = True) -> str:
        js = {
            'task': self.task.value,
            'data': {
                'request_id': self.request_id,
                'state': self.state.value,
                'currency_in_name': self.currency_in_name,
                'currency_in_amount': self.currency_in_amount,
                'currency_out_name': self.currency_out_name,
                'currency_out_amount': self.currency_out_amount,
                'error': self.error,

            }
        }
        js_str = json.dumps(js)
        return TramaWriter.write([
            (self.timestamp, 13),
            (js_str, len(js_str)),
        ], sign)

    @classmethod
    def from_trama(cls, trama: str, with_signature: bool = True):
        trama_reader = TramaReader(trama, with_signature)
        timestamp = trama_reader.read(13),
        js = trama_reader.get_unread()
        data_ = json.loads(js)
        task = cls.TASK_NAME(data_['task'])
        data = data_['data']
        quote_service_internal_execute = cls(
            timestamp=timestamp,
            task=task,
            request_id=data['request_id'],
            state=cls.STATE(data['state']),
            currency_in_name=data['currency_in_name'],
            currency_in_amount=data['currency_in_amount'],
            currency_out_name=data['currency_out_name'],
            currency_out_amount=data['currency_out_amount'],
            error=data['error'],
        )
        return quote_service_internal_execute
