#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
* Author Dominik Symonowicz
* WWW:	https://dominiksymonowicz.com/welcome
* IT BLOG:	https://dominiksymonowicz.blogspot.co.uk
* Github:	https://github.com/pastorcmentarny
* Google Play:	https://play.google.com/store/apps/developer?id=Dominik+Symonowicz
* LinkedIn: https://www.linkedin.com/in/dominik-symonowicz
"""
import logging
import logging.config
import re
from datetime import date
from datetime import datetime
from datetime import timedelta

from common.gobshite_exception import GobshiteException

stats_log = logging.getLogger('stats')
logger = logging.getLogger('app')


def as_3_digit_number(index: int) -> str:
    return f"{index:03d}"


def convert_list_to_dict(source: list) -> dict:
    return {as_3_digit_number(index + 1): source[index] for index in range(0, len(source))}


def get_date_as_filename(name: str, file_type: str, dt: datetime) -> str:
    return f"{name}-{dt.year}-{dt.month:02d}-{dt.day:02d}.{file_type}"


def get_date_with_time_as_filename(name: str, file_type: str, dt: datetime) -> str:
    return f"{name}-{dt.year}-{dt.month:02d}-{dt.day:02d}-{dt.hour:02d}{dt.minute:02d}{dt.second:02d}.{file_type}"


def get_filename_from_year_month_day(name: str, file_type: str, year: int, month: int, day: int) -> str:
    return f"{name}-{year}-{month:02d}-{day:02d}.{file_type}"


def get_filename_for_warnings(year, month, day):
    return f"warnings.log.{year}-{month:02d}-{day:02d}"


def get_filename_for_stats(year, month, day):
    return f"stats.log.{year}-{month:02d}-{day:02d}"


def get_yesterday_date() -> datetime:
    today = datetime.now()
    return today - timedelta(days=1)


def get_two_days_ago_date() -> datetime:
    today = datetime.now()
    return today - timedelta(days=2)


def get_dates_for_last_7_days() -> list:
    today = datetime.now()
    days = []
    for i in range(1, 8):
        days.append(today - timedelta(days=i))
    return days


def get_timestamp_title(with_time: bool = True) -> str:
    if with_time:
        pattern = "%Y-%m-%d %H:%M:%S"
    else:
        pattern = "%Y-%m-%d"
    return datetime.now().strftime(pattern)


def get_timestamp_file() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def get_timestamp_key(dt: datetime = datetime.now()) -> str:
    return dt.strftime("%m%d")


def to_hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)


# TODO change return from str to float
def get_float_number_from_text(text: str) -> str:
    return re.sub('[^0-9.]', '', text)


def get_int_number_from_text(text: str) -> int:
    return int(re.sub('[^0-9]', '', text))


def fix_nulls(data):
    for line in data:
        yield line.replace('\0', '')


def is_file_older_than_5_minutes(filename: str) -> bool:
    year = int(filename[0:4])
    month = int(filename[4:6])
    day = int(filename[6:8])
    hour = int(filename[9:11])
    minut = int(filename[11:13])
    second = int(filename[13:15])
    print(year)
    print(month)
    print(day)
    print(hour)
    print(month)
    print(second )
    last = datetime(year, month, day, hour, minut, second)
    now = datetime.now()
    time_delta = now - last
    return (time_delta.seconds / 60) > 5


def is_timestamp_older_than_5_minutes(timestamp: str) -> bool:
    now = datetime.now()
    last = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
    time_delta = now - last
    return (time_delta.seconds / 60) > 5


color_name = {
    '#F0FFFF': 'azure ',
    '#F5F5DC': 'beige',
    '#000000': 'black',
    '#0000FF': 'blue',
    '#8A2BE2': 'blueviolet',
    '#A52A2A': 'brown',
    '#D2691E': 'chocolate',
    '#FF7F50': 'coral',
    '#6495ED': 'cornflowerblue',
    '#00FFFF': 'cyan',
    '#00008B': 'dark blue',
    '#008B8B': 'dark cyan',
    '#006400': 'dark green ',
    '#A9A9A9': 'dark grey ',
    '#FF8C00': 'dark orange',
    '#8B0000': 'dark red',
    '#9400D3': 'dark violet',
    '#B22222': 'firebrick ',
    '#228B22': 'forest green',
    '#F8F8FF': 'ghost white',
    '#FFD700': 'gold',
    '#808080': 'grey',
    '#008000': 'green',
    '#ADFF2F': 'green yellow',
    '#F0FFF0': 'honeydew',
    '#FF69B4': 'hotpink',
    '#4B0082': 'indigo',
    '#FFFFF0': 'ivory',
    '#E6E6FA': 'lavender',
    '#7CFC00': 'lawngreen',
    '#ADD8E6': 'light blue',
    '#E0FFFF': 'light cyan',
    '#90EE90': 'light green',
    '#D3D3D3': 'light grey',
    '#00FF00': 'lime',
    '#FF00FF': 'magenta',
    '#800000': 'maroon',
    '#191970': 'midnight blue',
    '#FFE4E1': 'mistyrose',
    '#000080': 'navy',
    '#808000': 'olive',
    '#FFA500': 'orange',
    '#FF4500': 'orange red',
    '#FFC0CB': 'pink',
    '#DDA0DD': 'plum',
    '#800080': 'purple',
    '#FF0000': 'red',
    '#FA8072': 'salmon',
    '#2E8B57': 'seashell',
    '#A0522D': 'sienna',
    '#C0C0C0': 'silver',
    '#87CEEB': 'skyblue',
    '#708090': 'slate grey',
    '#FFFAFA': 'snow',
    '#008080': 'teal',
    '#FF6347': 'tomato',
    '#40E0D0': 'turquoise',
    '#EE82EE': 'violet',
    '#FFFFFF': 'white',
    '#FFFF00': 'yellow'
}

tube_color_name = {
    '#B26200': 'Bakerloo line',
    '#DC241F': 'Central line',
    '#FFD429': 'Circle line',
    '#007D32': 'District line',
    '#F4A9BE': 'Hammersmith & City line',
    '#A1A5A7': 'Jubilee line',
    '#9B0058': 'Metropolitan line',
    # Northern line not part of this as is  ... #000000
    '#0019A8': 'Piccadilly line',
    '#0098D8': 'Victoria line',
    '#93CEBA': 'Waterloo & City line'
}


def get_color_name(hex_colour: str):
    hex_colour = hex_colour.upper()
    if hex_colour in tube_color_name:
        stats_log.info(tube_color_name[hex_colour] + ' color')
        return tube_color_name[hex_colour].capitalize()
    if hex_colour in color_name:
        return color_name[hex_colour].capitalize()
    else:
        return hex_colour


def clean_list_from_nones(dirty_list: list) -> list:
    clean_list = []
    for item in dirty_list:
        if item is not None:
            clean_list.append(item)
    return clean_list


def merge_two_dictionaries(first: dict, second: dict) -> dict:
    second.update(first)
    return second


def setup_test_logging():
    logging.basicConfig(level=logging.DEBUG)
    logging.debug('Running test logging')


def convert_bytes_to_megabytes(size_in_bytes: int) -> int:
    return int(size_in_bytes / 1000 / 1000)


def to_multiline(lines: list) -> str:
    text = ''
    for line in lines:
        text += line + '\n'
    return text


def get_date_as_folders() -> str:
    today = date.today()
    year = today.year
    month = today.month
    day = today.day
    return "\\{}\\{:02x}\\{:02x}\\".format(year, month, day)


def _is_valid_event_time(event) -> bool:
    if not event or event.isspace():
        return False
    time_with_title_split = event.split(' - ')

    if len(time_with_title_split) > 2 or len(time_with_title_split) < 2:
        return False

    hour_with_minutes = time_with_title_split[0].split(':')
    if len(hour_with_minutes) > 2 or len(hour_with_minutes) < 2:
        return False

    hour = hour_with_minutes[0]
    minute = hour_with_minutes[1]

    if not hour.isdecimal():
        return False

    if not minute.strip().isdecimal():
        return False

    if len(hour) > 2 or len(minute) > 2 or len(minute) < 2:
        return False
    if int(hour) > 23 or int(minute) > 59:
        return False
    return True


def convert_time_to_minutes(event: str) -> int:
    if not _is_valid_event_time(event):
        raise GobshiteException
    event_time = event.split(' - ')[0].split(':')
    hours = int(event_time[0])
    minutes = int(event_time[1].strip())
    return hours * 60 + minutes


def is_weekend_day(today: datetime) -> bool:
    day_of_the_week = today.weekday()
    return day_of_the_week > 4


def log_error_count(errors:list):
    number_of_errors = len(errors)
    if number_of_errors >= 2:
        logger.error('Found {} error(s).'.format(len(errors)))
    elif number_of_errors > 0:
        logger.warning('Found {} error(s).'.format(len(errors)))
    else:
        logger.debug('No errors found.')
