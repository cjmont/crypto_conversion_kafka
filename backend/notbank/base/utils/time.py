from datetime import datetime
from time import time


def get_timestamp() -> str:
    return str(int(time()*1000))


def str_timestamp_from_datetime(date_time: datetime) -> str:
    return str(int(date_time.timestamp()*1000))


def datetime_from_timestamp(timestamp: str) -> datetime:
    return datetime.fromtimestamp(int(timestamp)/1000)
