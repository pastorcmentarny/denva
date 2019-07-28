import datetime
from datetime import timedelta


def get_date_as_filename(name: str, type: str, dt: datetime) -> str:
    return f"{name}-{dt.year}-{dt.month:02d}-{dt.day:02d}.{type}"


def get_yesterday_date() -> datetime:
    today = datetime.datetime.now()
    return today - timedelta(days=1)
