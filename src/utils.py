from datetime import datetime
from datetime import timedelta
import re


def get_date_as_filename(name: str, file_type: str, dt: datetime) -> str:
    return f"{name}-{dt.year}-{dt.month:02d}-{dt.day:02d}.{file_type}"


def get_filename_from_year_month_day(name: str, file_type: str, year: int, month: int, day: int) -> str:
    return f"{name}-{year}-{month:02d}-{day:02d}.{file_type}"


def get_filename_for_warnings(year, month, day):
    return f"warnings.log.{year}-{month:02d}-{day:02d}"


def get_yesterday_date() -> datetime:
    today = datetime.now()
    return today - timedelta(days=1)


def get_timestamp_title() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def to_hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)


def get_float_number_from_text(cpu_temp: str) -> str:
    return re.sub('[^0-9.]', '', cpu_temp)
