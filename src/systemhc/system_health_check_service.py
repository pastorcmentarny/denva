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

import logging
from datetime import datetime

import config
import dom_utils
from common import app_timer, data_writer, data_loader

logger = logging.getLogger('app')


def save(data: dict):
    try:
        data_writer.save_dict_data_as_json(config.get_system_hc(), data)
    except Exception as exception:
        logger.error(f'Unable to save file with system healthcheck due to {exception}', exc_info=True)


def load() -> dict:
    system_hc_path = config.get_system_hc()
    try:
        return data_loader.load_json_data_as_dict_from(system_hc_path)
    except Exception as exception:
        logger.error(
            f'Unable to load file with system healthcheck as due to {exception} using path {system_hc_path}',
            exc_info=True)
        logger.info('Recreating healthcheck data')
        return hc_fix.copy()


def to_timestamp(now: datetime) -> str:
    return str(
        f'{now.year}{now.month:02d}{now.day:02d}{now.hour:02d}{now.minute:02d}{now.second:02d}')


def update_to_now_for_all():
    now = datetime.now()
    system = {
        'denva': {
            'app': to_timestamp(now),
            'ui': to_timestamp(now),
            'device': 'OK'
        },
        'denva2': {
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


# FIXM
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
        logger.error(f'Unable to check if system is up due to {exception}', exc_info=True)
        return config.UNKNOWN


def get_status(previous_datetime):
    if app_timer.is_it_time(previous_datetime, 2 * 60):
        if app_timer.is_it_time(previous_datetime, 5 * 60):
            return 'DOWN'
        else:
            return 'WARN'
    return 'UP'


def is_camera_up(device: str, app_type: str):
    if config.is_sky_camera_on():
        is_up(device, app_type)
    else:
        return 'OFF'


def is_radar_up(device: str, app_type: str):
    if config.is_radar_on():
        is_up(device, app_type)
    else:
        return 'OFF'


def get_system_healthcheck():
    return {
        'denva': {
            'app': is_up('denva', 'app'),
            'ui': is_up('denva', 'ui')
        },
        'server': {
            'app': is_up('server', 'app'),
            'ui': is_up('server', 'ui')
        },
        'knyszogar': {
            'cctv': is_camera_up('knyszogar', 'cctv'),
            'radar': is_radar_up('knyszogar', 'radar'),
            'digest': is_up('knyszogar', 'digest'),

        }
    }
