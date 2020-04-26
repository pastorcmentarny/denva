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
import platform

from common import dom_utils

settings = {
    "mode": 'dev',
    "sensors": {
        "motion": {
            "shaking": 1000,
            "sensitivity": 8,
            "noOfFlashes": 5
        }
    },
    "paths": {
        "base": {
            'dev': 'D:\Projects\denva\src\\',
            'server': 'E:\denva\src\\'
        },
        "frame": {
            'dev': 'D:\ds-lpd-server\cctv\\1',
            'server': 'E:\\frame\\'
        },
        "backup": "D:\\denva\\backup\\",
        "photosPath": "/mnt/data/photos/",
        "tubeAndTrainsPath": "D:\\denva\\data\\tubetrains\\",
        "events": {
            "dev": "D:\\denva\\events.json",
            "server": "E:\\denva\\events.json"
        },
        "bin": "D:\\ds-lpd-server\\data-bin\\",
        "cctv-backup": ["D:\\ds-lpd-server\\cctv", "D:\\ds-lpd-server\\backup"],
        "chinese-dictionary": {
            'dev': "D:\Projects\denva\src\data\dictionary.txt",
            'server': "E:\denva\src\data\dictionary.txt"
        },
        "server_drive": "D:\\Projects\\denva\\src\\data\\dictionary.txt",
        "zeroeight": "",
    },
    "sensor": {
        "cpu_temp_warn": 60,
        "cpu_temp_error": 70,
        "cpu_temp_fatal": 80
    },
    "system": {
        "memory_available": 250 * 1024 * 1024,  # 250MB
        "free_space": 500,
        "ip": "http://192.168.0.200:5000"
    },
    "options": {
        "inChina": False
    },
    "urls": {
        "server": "http://192.168.0.200:5000",
        "denva": "http://192.168.0.201:5000",
        "enviro": "http://192.168.0.202:5000",
        "delight": "http://192.168.0.203:5000"
    },
    "logs": {
        'dev_app': 'D:\GitHub\denva\src\configs\dev_log_app_config.json',
        'dev_ui': 'D:\GitHub\denva\src\configs\dev_log_ui_config.json',
        'server_app': 'E:\denva\src\configs\server_log_app_config.json',
        'server_ui': 'E:\denva\src\configs\server_log_ui_config.json',
        'denva_app': '/home/pi/denva-master/src/configs/log_app_config.json',
        'denva_ui': '/home/pi/denva-master/src/configs/log_ui_config.json',
        'denviro_app': '/home/pi/denva-master/src/configs/log_app_config.json',
        'denviro_ui': '/home/pi/denva-master/src/configs/log_ui_config.json',
        'delight_app': '/home/pi/denva-master/src/configs/log_app_config.json',
        'delight_ui': '/home/pi/denva-master/src/configs/log_ui_config.json',
        'hc': '/home/pi/denva-master/src/configs/log_config.json',
        'log_app': '/home/pi/logs/logs.log',
        'log_hc': '/home/pi/logs/healthcheck.log',
        'log_ui': '/home/pi/logs/server.log'
    },
    "informationData": {
        'dev': 'D:\Projects\denva\src\data\information.json',
        'server': 'E:\denva\src\data\information.json'
    },
    "test": {
        'slow_test': False
    }
}
PI_PATH = '/home/pi/logs/'
NETWORK_PATH = '/mnt/data/sensors/'


def get_log_path_for(log_type: str) -> str:
    return settings['logs'][log_type]


def get_environment_log_path_for(where: str) -> str:
    env_type = settings['mode']
    if env_type == 'dev':
        return settings['logs']['dev_' + where]
    if env_type == 'server':
        return settings['logs']['server_' + where]
    return settings['logs']['{}_{}'.format(env_type, where)]


def get_information_path() -> str:
    if settings["mode"] == 'dev':
        return settings['informationData']['dev']
    else:
        return settings['informationData']['server']


def load_cfg() -> dict:
    return settings


def get_healthcheck_ip() -> str:
    config = load_cfg()
    return config['system']['ip']


def get_current_warnings_url_for(service: str) -> str:
    config = load_cfg()
    return "{}/warns/now".format(config['urls'][service])


def get_options() -> dict:
    config = load_cfg()
    return config['options']


def get_path_for_personal_events() -> str:
    mode = settings['mode']
    return settings['paths']['events'][mode]


def get_path_for_data_bin() -> str:
    config = load_cfg()
    return config['paths']['bin']


def get_path_for_cctv_backup() -> list:
    config = load_cfg()
    return config['paths']['cctv-backup']


def get_path_to_chinese_dictionary() -> str:
    if settings["mode"] == 'dev':
        return settings['paths']['chinese-dictionary']['dev']
    else:
        return settings['paths']['chinese-dictionary']['server']


def get_irregular_verbs_path() -> str:
    mode = settings['mode']
    return settings['paths']['base'][mode] + 'data/irregular_verbs.txt'


# TODO refactor it
def get_path_for_information_backup() -> str:
    path = ":\\denva\\"
    if settings['mode'] == 'server':
        return 'e' + path
    return 'd' + path


def set_mode_to(mode: str):
    settings['mode'] = mode
    if platform.node() == 'DomL5' or platform.node() == 'DomAsusG':
        settings['mode'] = 'dev'
    print('The mode is set to {}'.format(settings['mode']))


def get_mode() -> str:
    return settings['mode']


def get_memory_available_threshold():
    return settings['system']['memory_available']


def get_disk_space_available_threshold():
    return settings['system']['free_space']


def get_system_drive() -> str:
    mode = get_mode()
    print(mode)
    if mode == 'dev':
        return 'D:'
    elif mode == 'server':
        return 'E:'
    else:
        return '/'


def run_slow_test() -> bool:
    return settings['test']['slow_test']


def get_shaking_level():
    return settings['sensors']['motion']['shaking']


def get_sensitivity():
    return settings['sensors']['motion']['sensitivity']


def get_data_path() -> str:
    return get_system_drive() + '\\denva\\data\\'


def get_sensor_log_file_for(year: int, month: int, day: int, sensor_filename: str = 'sensor-log') -> str:
    path = '/home/pi/logs/' + dom_utils.get_filename_from_year_month_day(sensor_filename, 'csv', year, month, day)
    return path
