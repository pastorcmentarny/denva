import logging

import config
import dom_utils
from db import db_service
from datetime import datetime

ENCODING = config.ENCODING

logger = logging.getLogger('app')


def update_for(who: dict):
    service_name = f"{who['device']}_{who['app_type']}"
    device_name = f"{who['device']}_device"
    db_service.set_device_on(device_name)
    db_service.update_for(service_name)


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
        previous_datetime = datetime(dom_utils.to_int(previous[0:4]), dom_utils.to_int(previous[4:6]),
                                     dom_utils.to_int(previous[6:8]),
                                     dom_utils.to_int(previous[8:10]), dom_utils.to_int(previous[10:12]),
                                     dom_utils.to_int(previous[12:14]))
        return __get_status(previous_datetime)
    except Exception as exception:
        logger.error(f'Unable to check if system is up due to {exception}', exc_info=True)
        return config.UNKNOWN


def get_device_status_for(device: str, app_type: str):
    try:
        name = device + "_" + app_type
        return db_service.get_status_for(name)
    except Exception as exception:
        logger.error(f'Unable to check if system is up due to {exception}', exc_info=True)
        return config.UNKNOWN


# TODO multiple power state
def update_device_power_state_for(who):
    logger.warning(f'Not implemented yet. Data sent: {who}')
    # I need script to run before reboot or shutdown first
