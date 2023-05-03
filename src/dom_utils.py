#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
* Author Dominik Symonowicz
* WWW:	https://dominiksymonowicz.com/welcome
* IT BLOG:	https://dominiksymonowicz.blogspot.co.uk
* GitHub:	https://github.com/pastorcmentarny
* Google Play:	https://play.google.com/store/apps/developer?id=Dominik+Symonowicz
* LinkedIn: https://www.linkedin.com/in/dominik-symonowicz
"""
import json
import logging
import re
import socket
from datetime import date
from datetime import datetime
from datetime import timedelta

import config
import requests

from common.gobshite_exception import GobshiteException

SERVER_IP = "http://192.168.0.200:5000/"

logger = logging.getLogger('app')

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}


def as_3_digit_number(index: int) -> str:
    return f"{index:03d}"


def convert_list_to_dict(source: list) -> dict:
    return {as_3_digit_number(index + 1): source[index] for index in range(0, len(source))}


def get_date_for_today() -> str:
    dt = datetime.now()
    return f"{dt.year}-{dt.month:02d}-{dt.day:02d}"


def get_today_date_as_filename(name: str, file_type: str) -> str:
    return get_date_as_filename(name,file_type,datetime.now())

def get_date_as_filename(name: str, file_type: str, dt: datetime) -> str:
    return f"{name}-{dt.year}-{dt.month:02d}-{dt.day:02d}.{file_type}"


def get_date_with_time_as_filename(name: str, file_type: str, dt: datetime) -> str:
    return f"{name}-{dt.year}-{dt.month:02d}-{dt.day:02d}-{dt.hour:02d}{dt.minute:02d}{dt.second:02d}.{file_type}"


def get_filename_from_year_month_day(name: str, file_type: str, year: int, month: int, day: int) -> str:
    return f"{name}-{year}-{month:02d}-{day:02d}.{file_type}"


def get_filename_for_warnings(year: str, month: str, day: str):
    return f"warnings.log.{int(year)}-{int(month):02d}-{int(day):02d}"


def get_filename_for_stats(year, month, day):
    return f"stats.log.{int(year)}-{int(month):02d}-{int(day):02d}"


def get_date_as_text(selected_date: datetime):
    return f'{selected_date.day:02d}-{selected_date.month:02d}-{selected_date.year} at {selected_date.hour}:{selected_date.minute}'


# TODO rename it to datetime
def get_yesterday_date() -> datetime:
    today = datetime.now()
    return today - timedelta(days=1)


# TODO rename it to date
def get_yesterday_date_as_date() -> date:
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    return yesterday.date()


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
    minute = int(filename[11:13])
    second = int(filename[13:15])
    last = datetime(year, month, day, hour, minute, second)
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
        logger.info(tube_color_name[hex_colour] + ' color')
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


def convert_bytes_to_megabytes(size_in_bytes: int) -> int:
    return int(size_in_bytes / 1000 / 1000)


def convert_megabytes_to_bytes(size_in_mb: int) -> int:
    return int(size_in_mb / 1000 / 1000)


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
    return "{}/{:02d}/{:02d}/".format(year, month, day)


def get_date_as_folders_linux() -> str:
    return get_date_as_folders_for(date.today())


def get_date_as_folders_for(specified_data: date):
    year = specified_data.year
    month = specified_data.month
    day = specified_data.day
    return "{}/{:02d}/{:02d}/".format(year, month, day)


def get_date_as_folders_for_today():
    return get_date_as_folders_for(datetime.today())


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
        logger.error(f'Time not valid for {event}')
        raise GobshiteException
    event_time = event.split(' - ')[0].split(':')
    hours = int(event_time[0])
    minutes = int(event_time[1].strip())
    return hours * 60 + minutes


def is_weekend_day(today: datetime) -> bool:
    day_of_the_week = today.weekday()
    return day_of_the_week > 4


def to_datetime(source: date) -> datetime:
    return datetime.combine(source, datetime.min.time())


def get_ip() -> str:
    return socket.gethostbyname(socket.gethostname())


def to_int(number_as_string: str) -> int:
    if number_as_string == '' or (number_as_string is None) or number_as_string == '00' or number_as_string == '0':
        return 0
    return int(number_as_string.lstrip('0'))


def post_healthcheck_beat(device: str, app_type: str):
    url = "%s:5000/shc/update" % config.SERVER_IP
    json_data = {'device': device, 'app_type': app_type}
    print(f'Post healthcheck with {json_data}')
    try:
        with requests.post(url, json=json_data, timeout=2, headers=HEADERS) as response:
            response.json()
            response.raise_for_status()
    except Exception as whoops:
        print('There was a problem: {} using url {}, device {} and app_type {}'.format(whoops, url, device, app_type))
        logger.warning(
            'There was a problem: {} using url {}, device {} and app_type {}'.format(whoops, url, device, app_type))


def setup_logging(app_name: str, debug_mode: bool = False):
    print('Setting logs ...')
    if debug_mode:
        logging_level = logging.DEBUG

    else:
        logging_level = logging.WARN

    logging_format = '%(levelname)s :: %(asctime)s :: %(message)s'
    logging_filename = f'/home/ds/logs/{app_name}-{date.today()}.txt'
    logging.basicConfig(level=logging_level, format=logging_format, filename=logging_filename)
    logging.captureWarnings(True)
    logging.info(f'Logging setup complete with log level set to: {logging_level})')
    print(f'Logs setup completed (Level: {logging_level})')


def setup_test_logging(app_name: str, debug_mode: bool = False):
    print('Setting logs ...')
    if debug_mode:
        logging_level = logging.DEBUG

    else:
        logging_level = logging.WARN

    logging_format = '%(levelname)s :: %(asctime)s :: %(message)s'
    logging_filename = f'/home/pi/knyszogardata/logs/{app_name}-{date.today()}.txt'
    logging.basicConfig(level=logging_level, format=logging_format, filename=logging_filename)
    logging.captureWarnings(True)
    logging.info(f'Logging setup complete with log level set to: {logging_level})')
    print(f'Logs setup completed (Level: {logging_level})')


def load_cfg() -> dict:
    with open('/home/pi/email.json', 'r') as email_config:
        return json.load(email_config)
