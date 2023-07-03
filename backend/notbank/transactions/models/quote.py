
from decimal import Decimal
import uuid

from django.db import models
from notbank.base.models.base import CommonModel
from notbank.base.utils.kafka.tramas.quote_listener import QuoteListener
from notbank.base.utils.time import datetime_from_timestamp


class Quote(CommonModel):
    request_id = models.UUIDField(unique = True, default=uuid.uuid4, editable=False)
    from_currency = models.CharField(max_length=8)
    from_amount = models.DecimalField(max_digits=36, decimal_places=18)
    to_currency = models.CharField(max_length=8)
    to_amount = models.DecimalField(max_digits=36, decimal_places=18)
    perfect_amount = models.DecimalField(max_digits=36, decimal_places=18)

    @classmethod
    def _from_quote_listener(cls, task: QuoteListener):
        return cls(
            created_at=datetime_from_timestamp(task.timestamp),
            request_id=task.request_id,
            from_currency=task.from_currency,
            from_amount=Decimal(task.from_amount),
            to_currency=task.to_currency,
            to_amount=Decimal(task.to_amount),
            perfect_amount=Decimal(task.perfect_amount),
        )

    @classmethod
    def from_quote_listener_trama(cls, trama: str, with_signature: bool = True):
        task = QuoteListener.from_trama(trama, with_signature)
        return cls._from_quote_listener(task)

