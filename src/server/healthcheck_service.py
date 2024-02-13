import logging
from db import db_service
from datetime import datetime

ENCODING = 'utf-8'

logger = logging.getLogger('app')


def update_for(who: dict):
    service_name = f"{who['device']}_{who['app_type']}"
    device_name = f"{who['device']}_device"
    db_service.set_device_on(device_name)
    db_service.update_for(service_name)


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
        name = device + "_" + app_type
        previous = db_service.get_status_for(name)
        previous_datetime = datetime(__to_int(previous[0:4]), __to_int(previous[4:6]),
                                     __to_int(previous[6:8]),
                                     __to_int(previous[8:10]), __to_int(previous[10:12]),
                                     __to_int(previous[12:14]))
        return __get_status(previous_datetime)
    except Exception as exception:
        logger.error('Unable to check if system is up due to {}'.format(exception), exc_info=True)
        return "UNKNOWN"


def get_device_status_for(device: str, app_type: str):
    try:
        name = device + "_" + app_type
        return db_service.get_status_for(name)
    except Exception as exception:
        logger.error('Unable to check if system is up due to {}'.format(exception), exc_info=True)
        return "UNKNOWN"


# TODO multiple power state
def update_device_power_state_for(who):
    logger.warning(f'Not implemented yet. Data sent: {who}')
    # I need script to run before reboot or shutdown first
