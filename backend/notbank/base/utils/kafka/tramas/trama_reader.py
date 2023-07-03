from notbank.base.utils.kafka.authentication import check_valid_signature
from notbank.base.utils.kafka.tramas.exceptions import (
    TramaFormatException, TramaValidationException)

class TramaReader:
    _pos: int
    _back_pos: int
    _trama: str

    def __init__(self, trama: str, with_signature: bool = True):
        self._pos = 0
        self._back_pos = len(trama)
        self._trama = trama
        if with_signature:
            self._validate_trama()

    def _validate_trama(self):
        """reads the signature (last 64 chars) and validates the data with it.
        Raises an exception if the signature is invalid"""
        signature = self.read_from_back(64)
        data = self.get_unread()
        if not check_valid_signature(data, signature):
            raise TramaValidationException()

    def is_done(self) -> bool:
        """checks if the trama is fully read."""
        return self._pos == self._back_pos

    def _check_valid_read_amount(self, amount: int):
        if self._pos + amount > self._back_pos:
            raise TramaFormatException(
                f'cannot read more than {self._back_pos-self._pos} characters of trama'
            )

    def read(self, amount: int, lstrip: bool = True) -> str:
        """reads from the left of the string"""
        self._check_valid_read_amount(amount)
        result = self._trama[self._pos:self._pos + amount]
        self._pos = self._pos + amount
        if lstrip:
            return result.lstrip()
        return result

    def read_from_back(self, amount: int, lstrip: bool = True) -> str:
        """reads from the right of the string"""
        self._check_valid_read_amount(amount)
        result = self._trama[self._back_pos-amount:self._back_pos]
        self._back_pos = self._back_pos - amount
        if lstrip:
            return result.lstrip()
        return result

    def get_unread(self):
        """gets the unread part of the string.
        the returned part does not count as read"""

        return self._trama[self._pos:self._back_pos]


def validate_trama(trama: str):
    TramaReader(trama, with_signature=True)
