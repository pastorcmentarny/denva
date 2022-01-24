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
import platform
from pathlib import Path

import dom_utils

SERVER_IP = 'http://192.168.0.200'
PI_HOME_DIR = '/home/pi/'
PI_PROJECT_PATH = f'{PI_HOME_DIR}denva-master/src'
PI_CONFIG_PATH = f'{PI_HOME_DIR}configs/'
PI_DATA_PATH = f'{PI_HOME_DIR}data/'
PI_LOGS_PATH = f'{PI_HOME_DIR}logs/'
PI_SENSORS_DATA_PATH = '/mnt/data/sensors/'

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
        "frame": f'{PI_HOME_DIR}/frame/',
        "backup": f'{PI_HOME_DIR}backup/',
        "photosPath": "/mnt/data/photos/",  # TODO change it
        "events": f'{PI_HOME_DIR}events.json',
        "chinese-dictionary": f'{PI_DATA_PATH}dictionary.txt',
        "overseer_mode": f'{PI_HOME_DIR}overseer_mode.txt'
    },
    "sensor": {
        "cpu_temp_warn": 60,
        "cpu_temp_error": 70,
        "cpu_temp_fatal": 80
    },
    "system": {
        "memory_available": 250 * 1024 * 1024,  # 250MB
        "free_space": 500,
        "ip": "{SERVER_IP}:5000"
    },
    "options": {
        "inChina": False
    },
    "urls": {
        "server": f'{SERVER_IP}:5000',
        "denva": "http://192.168.0.201:5000",
        "enviro": "http://192.168.0.202:5000",
        "delight": f'{SERVER_IP}:5000',
        "dump1090_data": "http://192.168.0.201:16601/data.json"
    },
    "latency": {
        "max": 200,
        "max-slow": 1000
    },
    "logs": {
        'dev_app': f'{PI_CONFIG_PATH}dev_log_app_config.json',
        'dev_ui': f'{PI_CONFIG_PATH}dev_log_ui_config.json',
        'dev_ddd': f'{PI_CONFIG_PATH}dev_log_app_config.json',
        'server_app': f'{PI_CONFIG_PATH}server_log_app_config.json',
        'server_ui': f'{PI_CONFIG_PATH}server_log_ui_config.json',
        'denva_app': f'{PI_CONFIG_PATH}log_app_config.json',
        'denva_ui': f'{PI_CONFIG_PATH}log_ui_config.json',
        'denviro_app': f'{PI_CONFIG_PATH}log_app_config.json',
        'denviro_ui': f'{PI_CONFIG_PATH}log_ui_config.json',
        'delight_app': f'{PI_CONFIG_PATH}log_app_config.json',
        'delight_ui': f'{PI_CONFIG_PATH}log_ui_config.json',
        'hc': f'{PI_CONFIG_PATH}log_config.json',
        'log_app': f'{PI_LOGS_PATH}logs.log',
        'log_hc': f'{PI_LOGS_PATH}healthcheck.log',
        'log_ui': f'{PI_LOGS_PATH}server.log',
        'ddd': f'{PI_CONFIG_PATH}log_ddd_config.log',
        'cctv': f'{PI_CONFIG_PATH}log_cctv_config.json',
        'overseer_mode': f'{PI_CONFIG_PATH}overseer_mode.json',
        'overseer': f'{PI_CONFIG_PATH}overseer.json',
    },
    "informationData": f'{PI_DATA_PATH}information.json',
    "test": {
        'slow_test': False
    }
}


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


def set_mode_to(mode: str):
    settings['mode'] = mode
    if platform.node() in ['DomL5', 'DomAsusG', 'DOM-DESKTOP']:
        settings['mode'] = 'dev'
    print('The mode is set to {}'.format(settings['mode']))


def get_mode() -> str:
    return settings['mode']


def get_memory_available_threshold():
    return settings['system']['memory_available']


def get_disk_space_available_threshold():
    return settings['system']['free_space']


def run_slow_test() -> bool:
    return settings['test']['slow_test']


def get_shaking_level():
    return settings['sensors']['motion']['shaking']


def get_sensitivity():
    return settings['sensors']['motion']['sensitivity']


def get_sensor_log_file_for(year: int, month: int, day: int, sensor_filename: str = 'sensor-log') -> str:
    path = PI_LOGS_PATH + dom_utils.get_filename_from_year_month_day(sensor_filename, 'csv', year, month, day)
    return path


def get_metrics_service_url():
    return settings["urls"]["server"] + "/metrics/add"


def get_warm_up_measurement_counter():
    return settings['sensors']['bme']['warm_up']


def get_radar_hc_url() -> str:
    return settings["urls"]["denva"] + "/hc/ar"


def get_system_hc_url() -> str:
    return settings["urls"]["delight"] + "/shc/update"


def get_system_hc_reboot_url() -> str:
    return settings["urls"]["delight"] + "/shc/reboot"


def get_service_on_off_url() -> str:
    return settings["urls"]["delight"] + "/shc/change"


def get_directory_path_for_aircraft() -> str:
    return PI_DATA_PATH


def get_url_for_dump1090():
    return settings["urls"]["dump1090_data"]


def max_latency(fast: bool = True):
    if fast:
        return settings["latency"]["max"]
    return settings["latency"]["max-slow"]


def get_system_hc() -> str:
    return str(Path('{}/hc.json'.format(PI_DATA_PATH)))


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
