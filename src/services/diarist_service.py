from datetime import datetime
from retrying import retry
import logging

"""
Service to write down all events that happen
"""
ENCODING = 'utf-8'
logger = logging.getLogger('www')


def add(new_entry):
    dt = datetime.now()
    path = f"diary-{dt.year}-{dt.month:02d}-{dt.day:02d}.txt"
    try:
        save_entry(new_entry, path)
    except Exception as exception:
        logger.error(f'Failed to save due to {exception}')


def __retry_on_exception(exception):
    logger.warning(f'Unable to save due to {exception}')
    return isinstance(exception, Exception)


def to_line(new_entry):
    now = datetime.now()
    timestamp = f'{now.year}{now.month:02d}{now.day:02d}{now.hour:02d}{now.minute:02d}{now.second:02d}'
    text = ''
    for element in new_entry:
        key, value = element, new_entry[element]
        text += f'{timestamp}::{value}'
    return text


@retry(retry_on_exception=__retry_on_exception, wait_exponential_multiplier=50, wait_exponential_max=1000,
       stop_max_attempt_number=5)
def save_entry(new_entry, path):
    with open(path, "a+", encoding=ENCODING) as diary_file:
        diary_file.write(to_line(new_entry))
        diary_file.write('\n')
