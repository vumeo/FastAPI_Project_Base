from datetime import datetime
from dateutil import parser
from typing import Union
from datetime import timedelta


def conv_str_to_iso8601(date_str: str, fmt: str = '%Y-%m-%d %H:%M:%S') -> str:
    date = datetime.strptime(date_str, fmt)
    return date.isoformat()


def conv_str_to_dt(date_str: str, fmt: str = '%Y-%m-%d %H:%M:%S') -> datetime:
    date = datetime.strptime(date_str, fmt)
    return date


def conv_dt_to_ts(dt: datetime) -> float:
    ts = datetime.timestamp(dt)
    return ts


def conv_dt_to_str(dt: Union[datetime, None], fmt: str = '%Y-%m-%d %H:%M:%S') -> Union[str, None]:
    if dt is None:
        return None
    dt_str = datetime.strftime(dt, fmt)
    return dt_str


def conv_str_to_ts(dt_str: str) -> float:
    dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
    ts = datetime.timestamp(dt)
    return ts


def conv_ts_to_str(ts):
    date = datetime.fromtimestamp(ts)
    date_str = datetime.strftime(date, '%Y-%m-%d %H:%M:%S')
    return date_str


def get_current_dt() -> datetime:
    now = datetime.now()
    return now


def get_current_ts() -> float:
    return conv_dt_to_ts(get_current_dt())


def get_start_of_day(dt: datetime) -> datetime:
    start_of_day = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    return start_of_day


def get_end_of_day(dt: datetime) -> datetime:
    end_of_day = dt.replace(hour=23, minute=59, second=59, microsecond=999999)
    return end_of_day


def normalize_dt_to_str_fmt(value: Union[str, datetime], target_fmt: str = '%Y-%m-%d %H:%M:%S') -> str:
    if isinstance(value, str):
        dt = parser.parse(value)
        return conv_dt_to_str(dt, fmt=target_fmt)
    elif isinstance(value, datetime):
        return conv_dt_to_str(value, fmt=target_fmt)

    dt = get_current_dt()
    return conv_dt_to_str(dt, fmt=target_fmt)


def is_dt_fmt(val: Union[str, datetime]) -> bool:
    try:
        if isinstance(val, datetime):
            return True
        parser.parse(val)
        return True
    except Exception:
        return False


def subtract_days_from_dt(dt: datetime, days: int) -> datetime:
    return dt - timedelta(days=days)


def months_between(date1: datetime, date2: datetime) -> int:
    months = (date2.year - date1.year) * 12 + (date2.month - date1.month)
    return abs(months)

def days_between(date1: datetime, date2: datetime) -> int:
    delta = date2 - date1
    return abs(delta.days)