import json
import logging
from datetime import datetime

ENCODING = 'utf-8'

logger = logging.getLogger('app')

healthcheck_path = '/home/pi/data/hc.json'


# TODO replace from data_file
def save_dict_data_as_json(path: str, data: dict):
    with open(path, "w+", encoding=ENCODING) as path_file:
        json.dump(data, path_file, ensure_ascii=False, indent=4)


# TODO replace from data_file
def load_json_data_as_dict_from(path: str) -> dict:
    with open(path, "r", encoding=ENCODING) as json_file:
        return json.load(json_file)


def __save(data: dict):
    try:
        save_dict_data_as_json(healthcheck_path, data)
    except Exception as exception:
        logger.error('Unable to save file with system healthcheck due to {}'.format(exception), exc_info=True)


def __load() -> dict:
    try:
        return load_json_data_as_dict_from(healthcheck_path)
    except Exception as exception:
        logger.error(
            'Unable to load file with system healthcheck as due to {} using path {}'.format(exception, healthcheck_path),
            exc_info=True)


def update_for(who: dict):
    # TODO validate it
    try:
        data = __load()
        now = datetime.now()
        data[who['device']][who['app_type']] = str(
            '{}{:02d}{:02d}{:02d}{:02d}{:02d}'.format(now.year, now.month, now.day, now.hour, now.minute, now.second))
        __save(data)
    except Exception as exception:
        logger.error('Unable to update healthcheck due to {}'.format(exception), exc_info=True)


# TODO move to dom_utils
def __to_int(number_as_string: str) -> int:
    if number_as_string == '' or (number_as_string is None) or number_as_string == '00' or number_as_string == '0':
        return 0
    return int(number_as_string.lstrip('0'))


def __is_it_time(previous_update_time: datetime, time_difference: int) -> bool:
    time_now = datetime.now()
    duration = time_now - previous_update_time
    duration_in_seconds = duration.total_seconds()
    return duration_in_seconds > time_difference


def __get_status(previous_datetime):
    if __is_it_time(previous_datetime, 2 * 60):
        if __is_it_time(previous_datetime, 5 * 60):
            return 'ERROR'
        else:
            return 'WARN'
    return 'OK'


def is_up(device: str, app_type: str) -> str:
    try:
        system = __load()
        previous = system[device][app_type]

        previous_datetime = datetime(__to_int(previous[0:4]), __to_int(previous[4:6]),
                                     __to_int(previous[6:8]),
                                     __to_int(previous[8:10]), __to_int(previous[10:12]),
                                     __to_int(previous[12:14]))

        return __get_status(previous_datetime)
    except Exception as exception:
        logger.error('Unable to check if system is up due to {}'.format(exception), exc_info=True)
        return "UNKNOWN"
