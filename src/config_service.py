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
from pathlib import Path

from common import dom_utils

settings = {
    "mode": 'dev',
    "sensors": {
        "cameras": {
            "cctv": False,
            "sky": False
        },
        "motion": {
            "shaking": 1000,
            "sensitivity": 8,
            "noOfFlashes": 5
        },
        "bme": {
            "warm_up": 10
        },
        "unicornhd": {
            "default_brightness": 0.3
        },
        "radar": False
    },
    "paths": {
        "base": {
            'dev': 'D:\Projects\denva\src\\',
            'server': 'd:\denva\src\\'
        },
        "frame": {
            'dev': 'D:\ds-lpd-server\cctv\\1',
            'server': 'd:\\frame\\'
        },
        "backup": "D:\\denva\\backup\\",
        "photosPath": "/mnt/data/photos/",
        "tubeAndTrainsPath": "D:\\denva\\data\\tubetrains\\",
        "events": {
            "dev": "D:\\denva\\events.json",
            "server": "d:\\denva\\events.json"
        },
        "cctv-backup": ["D:\\ds-lpd-server\\cctv", "D:\\ds-lpd-server\\backup"],
        "chinese-dictionary": {
            'dev': "D:\Github\denva\src\data\dictionary.txt",
            'server': "d:\denva\src\data\dictionary.txt"
        },
        "server_drive": "D:\\Projects\\denva\\src\\data\\dictionary.txt",
        "zeroeight": "",
        "overseer_mode": r"D:\overseer_mode.txt"
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
        "delight": "http://192.168.0.203:5000",
        "dump1090_data": "http://192.168.0.201:16601/data.json"
    },
    "latency": {
        "max": 200,
        "max-slow": 1000
    },
    "logs": {
        'dev_app': 'D:\GitHub\denva\src\configs\dev_log_app_config.json',
        'dev_ui': 'D:\GitHub\denva\src\configs\dev_log_ui_config.json',
        'dev_ddd': 'D:\GitHub\denva\src\configs\dev_log_app_config.json',
        'server_app': 'd:\denva\src\configs\server_log_app_config.json',
        'server_ui': 'd:\denva\src\configs\server_log_ui_config.json',
        'denva_app': '/home/pi/denva-master/src/configs/log_app_config.json',
        'denva_ui': '/home/pi/denva-master/src/configs/log_ui_config.json',
        'denviro_app': '/home/pi/denva-master/src/configs/log_app_config.json',
        'denviro_ui': '/home/pi/denva-master/src/configs/log_ui_config.json',
        'delight_app': '/home/pi/denva-master/src/configs/log_app_config.json',
        'delight_ui': '/home/pi/denva-master/src/configs/log_ui_config.json',
        'hc': '/home/pi/denva-master/src/configs/log_config.json',
        'log_app': '/home/pi/logs/logs.log',
        'log_hc': '/home/pi/logs/healthcheck.log',
        'log_ui': '/home/pi/logs/server.log',
        'ddd': '/home/pi/denva-master/src/configs/log_ddd_config.log',
        'cctv': '/home/pi/denva-master/src/configs/log_cctv_config.json',
        'overseer_mode' : 'd:\denva\src\configs\overseer_mode.json',
        'overseer' : 'd:\denva\src\configs\overseer.json'
    },
    "informationData": {
        'dev': 'D:\Projects\denva\src\data\information.json',
        'server': 'd:\denva\src\data\information.json'
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
    if where == 'overseer_mode':
        return settings['logs']['overseer_mode']
    if where == 'overseer':
        return settings['logs']['overseer']
    if where == 'cctv':
        return settings['logs']['cctv']

    if where == 'hc':
        return settings['logs']['hc']

    if where == 'ddd':
        if env_type == 'dev':
            return settings['logs']['dev_' + where]
        else:
            return settings['logs']['dev_' + where]

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

def get_path_for_backup() -> str:
    return settings['paths']['backup']

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
        return 'd' + path
    return 'd' + path


def set_mode_to(mode: str):
    settings['mode'] = mode
    if platform.node() in ['DomL5' , 'DomAsusG' , 'DOM-DESKTOP']:
        settings['mode'] = 'dev'
    print('The mode is set to {}'.format(settings['mode']))


def get_mode() -> str:
    return settings['mode']


def get_memory_available_threshold():
    return settings['system']['memory_available']


def get_disk_space_available_threshold():
    return settings['system']['free_space']


# TODO refactor it
def get_system_drive() -> str:
    mode = get_mode()
    if mode == 'dev':
        return 'D:'
    elif mode == 'server':
        return 'D:'
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


def get_report_path_at_server():
    path = ''
    if get_mode() == 'dev':
        path = "d:\\denva\\data\\reports\\"
    elif get_mode() == 'server':
        path = "d:\\denva\\data\\reports\\"
    return path

def get_measurment_service_url():
        return settings["urls"]["denva"] + "/hc/ar"


def get_warm_up_measurement_counter():
    return settings['sensors']['bme']['warm_up']


def get_radar_hc_url() -> str:
    return settings["urls"]["denva"] + "/hc/ar"


def get_system_hc_url() -> str:
    return settings["urls"]["delight"] + "/shc/update"


def get_system_hc_reboot_url() -> str:
    return settings["urls"]["delight"] + "/shc/reboot"


def get_service__hc_url() -> str:
    return settings["urls"]["delight"] + "/shc/off"


def get_directory_path_for_aircraft() -> str:
    if get_mode() == 'dev':
        return "D:\\denva\\data"
    else:
        return '/home/pi/data'


def get_url_for_dump1090():
    return settings["urls"]["dump1090_data"]


def max_latency(fast: bool = True):
    if fast:
        return settings["latency"]["max"]
    return settings["latency"]["max-slow"]


def get_system_hc() -> str:
    if get_mode() == 'dev':
        file = "D:\\denva\\data"
    else:
        file = '/home/pi/data'

    return str(Path('{}/hc.json'.format(file)))


def get_default_brightness_for_delight_display():
    return settings["sensors"]["unicornhd"]["default_brightness"]


def is_cctv_camera_on() -> bool:
    return settings["sensors"]["cameras"]["cctv"]


def is_sky_camera_on() -> bool:
    return settings["sensors"]["cameras"]["sky"]


def is_radar_on():
    return settings["sensors"]["radar"]


def get_overseer_mode_file_path():
    return settings["paths"]["overseer_mode"]
