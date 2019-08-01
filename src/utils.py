from datetime import datetime
from datetime import timedelta
import re


def get_date_as_filename(name: str, type: str, dt: datetime) -> str:
    return f"{name}-{dt.year}-{dt.month:02d}-{dt.day:02d}.{type}"


def get_yesterday_date() -> datetime:
    today = datetime.now()
    return today - timedelta(days=1)


def get_timestamp_title() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def to_hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)


def get_float_number_from_text(cpu_temp: str) -> str:
    return re.sub('[^0-9.]', '', cpu_temp)
