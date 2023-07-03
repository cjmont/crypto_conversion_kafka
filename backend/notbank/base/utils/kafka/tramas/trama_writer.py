from typing import List, Tuple

from notbank.base.utils.kafka import authentication
from notbank.base.utils.kafka.tramas.exceptions import TramaLengthException


class TramaWriter:

    @staticmethod
    def _rjust(value: str, length: int) -> str:
        """pads a value with white space at the left"""
        if length < len(value):
            raise TramaLengthException(
                f"needs to read {length} out of {len(value)} from {value}"
            )
        line = value.rjust(length)
        return line

    @staticmethod
    def write(data: List[Tuple[str, int]], sign: bool = True) -> str:
        """makes a trama out of dict data. uses the key as the data and the value for each key as the length of the field.
        by default signs the data and includes the signature in the trama at the end (last 64 chars)"""
        trama = ''.join([
            TramaWriter._rjust(atuple[0], atuple[1]) for atuple in data
        ])
        if sign:
            return trama + authentication.sign(trama)
        return trama
