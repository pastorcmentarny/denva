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
from datetime import datetime

import config
from common import app_timer, data_files
import dom_utils

logger = logging.getLogger('app')


def save(data: dict):
    try:
        data_files.save_dict_data_as_json(config_service.get_system_hc(), data)
    except Exception as exception:
        logger.error('Unable to save file with system healthcheck due to {}'.format(exception), exc_info=True)


def load() -> dict:
    system_hc_path = config_service.get_system_hc()
    try:
        return data_files.load_json_data_as_dict_from(system_hc_path)
    except Exception as exception:
        logger.error(
            'Unable to load file with system healthcheck as due to {} using path {}'.format(exception, system_hc_path),
            exc_info=True)


def update_hc_for(device: str, app_type: str):
    try:
        data = load()
        now = datetime.now()
        data[device][app_type] = str(
            '{}{:02d}{:02d}{:02d}{:02d}{:02d}'.format(now.year, now.month, now.day, now.hour, now.minute, now.second))
        save(data)
    except Exception as exception:
        logger.error('Unable to update healthcheck due to {}'.format(exception), exc_info=True)


def to_timestamp(now: datetime) -> str:
    return str(
        '{}{:02d}{:02d}{:02d}{:02d}{:02d}'.format(now.year, now.month, now.day, now.hour, now.minute, now.second))


def update_to_now_for_all():
    now = datetime.now()
    system = {
        'denva': {
            'app': to_timestamp(now),
            'ui': to_timestamp(now),
            'device': 'OK'
        },
        'denviro': {
            'app': to_timestamp(now),
            'ui': to_timestamp(now),
            'device': 'OK'
        },
        'delight': {
            'app': to_timestamp(now),
            'ui': to_timestamp(now),
            'device': 'OK'
        },
        'server': {
            'app': to_timestamp(now),
            'ui': to_timestamp(now),
            'device': 'OK'
        },
        'other': {
            'cctv': to_timestamp(now),
            'radar': to_timestamp(now),
            'digest': to_timestamp(now),

        }
    }
    save(system)


def is_up(device: str, app_type: str) -> str:
    try:
        system = load()
        previous = system[device][app_type]

        previous_datetime = datetime(dom_utils.to_int(previous[0:4]), dom_utils.to_int(previous[4:6]),
                                     dom_utils.to_int(previous[6:8]),
                                     dom_utils.to_int(previous[8:10]), dom_utils.to_int(previous[10:12]),
                                     dom_utils.to_int(previous[12:14]))

        return get_status(previous_datetime)
    except Exception as exception:
        logger.error('Unable to check if system is up due to {}'.format(exception), exc_info=True)
        return "UNKNOWN"


def get_status(previous_datetime):
    if app_timer.is_it_time(previous_datetime, 2 * 60):
        if app_timer.is_it_time(previous_datetime, 5 * 60):
            return 'DOWN'
        else:
            return 'WARN'
    return 'UP'


def is_camera_up(device: str, app_type: str):
    if config_service.is_sky_camera_on():
        is_up(device, app_type)
    else:
        return 'OFF'


def is_radar_up(device: str, app_type: str):
    if config_service.is_radar_on():
        is_up(device, app_type)
    else:
        return 'OFF'


def get_system_healthcheck():
    return {
        'denva': {
            'app': is_up('denva', 'app'),
            'ui': is_up('denva', 'ui')
        },
        'denviro': {
            'app': is_up('denviro', 'app'),
            'ui': is_up('denviro', 'ui')
        },
        'delight': {
            'app': is_up('delight', 'app'),
            'ui': is_up('delight', 'ui')
        },
        'server': {
            'app': is_up('server', 'app'),
            'ui': is_up('server', 'ui')
        },
        'other': {
            'cctv': is_camera_up('other', 'cctv'),
            'radar': is_radar_up('other', 'radar'),
            'digest': is_up('other', 'digest'),

        }
    }
