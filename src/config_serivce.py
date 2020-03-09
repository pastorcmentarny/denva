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
settings = {
    "mode": 'dev',
    "sensors": {
        "motion": {
            "sensitivity": 1000,
            "noOfFlashes": 5,
            "kedOnLength": 0.2,
            "kedOffLength": 0.05
        }
    },
    "paths": {
        "backup": "D:\\denva\\backup\\",
        "photosPath": "/mnt/data/photos/",
        "tubeAndTrainsPath": "D:\\denva\\data\\tubetrains\\",
        "events": "D:\\ds-lpd-server\\events.json",
        "bin": "D:\\ds-lpd-server\\data-bin\\",
        "cctv-backup": ["D:\\ds-lpd-server\\cctv", "D:\\ds-lpd-server\\backup"],
        "chinese-dictionary": {
            'dev': "D:\Projects\denva\src\data\dictionary.txt",
            'server': "E:\denva\src\data\dictionary.txt"
        },
        "server_drive": "D:\\Projects\\denva\\src\\data\\dictionary.txt"
    },
    "sensor": {
        "cpu_temp_warn": 60,
        "cpu_temp_error": 70,
        "cpu_temp_fatal": 80
    },
    "system": {
        "free_space": 500,
        "ip": "http://192.168.0.6:5000"
    },
    "options": {
        "inChina": False
    },
    "urls": {
        "server": "http://192.168.0.5:5000",
        "denva": "http://192.168.0.2:5000",
        "enviro": "http://192.168.0.4:5000"
    },
    "logs": {
        'dev': 'D:\Projects\denva\src\configs\dev_log_config.json',
        'server': 'E:\denva\logs\server_log_config.json',
        'denva': '/home/pi/denva-master/src/configs/log_config.json',
        'enviro': '/home/pi/denva-master/src/configs/log_config.json'
    },
    "informationData": {
        'dev': 'D:\Projects\denva\src\data\information.json',
        'server': 'E:\denva\src\data\information.json'
    }
}


def get_log_path_for(env_type: str) -> str:
    if settings["mode"] == 'dev':
        return settings['logs']['dev']
    else:
        return settings['logs'][env_type]

def get_information_path() -> str:
    if settings["mode"] == 'dev':
        return settings['informationData']['dev']
    else:
        return settings['informationData']['server']


def load_cfg() -> dict:
    return settings


def update_healthcheck(ip: str):
    settings['system']['ip'] = '{}'.format(ip)
    print(settings['system']['ip'])


def get_healthcheck_ip() -> str:
    config = load_cfg()
    return config['system']['ip']


def get_current_warnings_url_for(service: str) -> str:
    config = load_cfg()
    return "{}/warns/now".format(config['url'][service])


def get_options() -> dict:
    config = load_cfg()
    return config['options']


def get_path_for_personal_events() -> str:
    config = load_cfg()
    return config['paths']['events']


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
