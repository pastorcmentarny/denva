import logging
from datetime import datetime

import config_service
from common import dom_utils, app_timer, data_files

logger = logging.getLogger('app')


def save(data: dict):
    try:
        data_files.save_dict_data_as_json(config_service.get_system_hc(), data)
    except Exception as exception:
        logger.error('Unable to save system healthcheck due to {}'.format(exception), exc_info=True)


def load() -> dict:
    try:
        return data_files.load_json_data_as_dict_from(config_service.get_system_hc())
    except Exception as exception:
        logger.error('Unable to load system healthcheck due to {}'.format(exception), exc_info=True)


def update_hc_for(device: str, app_type: str):
    data = load()
    now = datetime.now()
    data[device][app_type] = str(
        '{}{:02d}{:02d}{:02d}{:02d}{:02d}'.format(now.year, now.month, now.day, now.hour, now.minute, now.second))
    save(data)


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
    system = load()
    previous = system[device][app_type]

    previous_datetime = datetime(dom_utils.to_int(previous[0:4]), dom_utils.to_int(previous[4:6]),
                                 dom_utils.to_int(previous[6:8]),
                                 dom_utils.to_int(previous[8:10]), dom_utils.to_int(previous[10:12]),
                                 dom_utils.to_int(previous[12:14]))

    return get_status(previous_datetime)


def get_status(previous_datetime):
    if app_timer.is_it_time(previous_datetime, 60):
        if app_timer.is_it_time(previous_datetime, 5 * 60):
            return 'DOWN'
        else:
            return 'WARN'
    return 'UP'


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
            'cctv': is_up('other', 'cctv'),
            'radar': is_up('other', 'radar'),
            'digest': is_up('other', 'digest'),

        }
    }



if __name__ == '__main__':
    config_service.set_mode_to('dev')
    print(get_system_healthcheck())
    update_to_now_for_all()
    result = load()
    print(get_system_healthcheck())
    print(result)
