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
import csv
from datetime import datetime
import json
import os.path
import logging
import logging.config
import sensor_log_reader
from pathlib import Path

import config_serivce
import utils

logger = logging.getLogger('app')


def load_cfg() -> dict:
    if config_serivce.load_cfg()['mode'] == 'dev':
        path = 'd:\denva\email.json'
    elif config_serivce.load_cfg()['mode'] == 'server':
        path = 'e:\denva\email.json'
    else:
        path = '/home/pi/email.json'  # actual cfg is different place
    with open(path, 'r') as email_config:
        return json.load(email_config)


def save_report(report: dict, file: str):
    report_file_path = '/home/pi/reports/{}'.format(file)
    logger.info('Saving report to {}'.format(report_file_path))
    with open(report_file_path, 'w+', encoding='utf-8') as report_file:
        json.dump(report, report_file, ensure_ascii=False, indent=4)


def load_report(report_date: str) -> dict:
    report_file_path = '/home/pi/reports/{}'.format(report_date)
    logger.info('Loading report from {}'.format(report_file_path))
    with open(report_file_path, 'r') as report_file:
        return json.load(report_file)


def load_warnings(path: str) -> list:
    file = open(path, 'r', newline='')
    content = file.readlines()
    content.insert(0, 'Warning counts: {}'.format(len(content)))
    return content


def load_stats(path: str) -> list:
    file = open(path, 'r', newline='')
    content = file.readlines()
    return content


def check_if_report_was_generated(report_date: str) -> bool:
    path = '/home/pi/reports/{}'.format(report_date)
    return os.path.isfile(path)


def add_enviro_measurement_to_file(file, data:dict):
    timestamp = datetime.now()
    csv_writer = csv.writer(file)
    csv_writer.writerow([timestamp,
                     data["temperature"], data["pressure"],  data["humidity"],
                     data["light"], data["proximity"], data["oxidised"], data["reduced"],
                     data["nh3"], data["pm1"], data["pm25"], data["pm10"],
                     ])
    file.close()


def store_enviro_measurement(data:dict):
    local_file = open(sensor_log_reader.get_enviro_sensor_log_file(), 'a+', newline='')
    add_enviro_measurement_to_file(local_file, data)
    try:
        server_file = open(sensor_log_reader.get_enviro_sensor_log_file_at_server(), 'a+', newline='')
        add_enviro_measurement_to_file(server_file, data)
        # if flag is true, set to false
    except IOError as exception:
        logger.warning(exception)
        # add flag to indicate that there is a problem


def add_measurement_to_file(file, data:dict, motion):
    timestamp = datetime.now()
    csv_writer = csv.writer(file)
    csv_writer.writerow([timestamp,
                         data['temp'], data['pressure'], data['humidity'], data['gas_resistance'],
                         data['colour'], data['aqi'],
                         data['uva_index'], data['uvb_index'],
                         data['motion'],
                         motion['ax'], motion['ay'], motion['az'],
                         motion['gx'], motion['gy'], motion['gz'],
                         motion['mx'], motion['my'], motion['mz'],
                         data['measurement_time'],
                         utils.get_float_number_from_text(data['cpu_temp']),
                         data['eco2'],
                         data['tvoc'],
                         ])
    file.close()


def store_measurement(data, motion):
    local_file = open(sensor_log_reader.get_sensor_log_file(), 'a+', newline='')
    add_measurement_to_file(local_file, data, motion)
    try:
        server_file = open(sensor_log_reader.get_sensor_log_file_at_server(), 'a+', newline='')
        add_measurement_to_file(server_file, data,motion)
        # if flag is true, set to false
    except IOError as exception:
        logger.warning(exception)
        # add flag to indicate that there is a problem


def setup_logging():
    path = config_serivce.get_log_path_for()
    if os.path.exists(path):
        with open(path, 'rt') as config_json_file:
            config = json.load(config_json_file)
        logging.config.dictConfig(config)
        logger.info('logs loaded from {}'.format(path))
    else:
        logging.basicConfig(level=logging.INFO)


def load_json_data_as_dict_from(path: str) -> dict:
    with open(path, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)

def save_dict_data_as_json(path: str,data: dict):
    with open(path, 'w', encoding='utf-8') as path_file:
        json.dump(data,path_file , ensure_ascii=False, indent=4)


def backup_information_data(data: dict):
    dt = datetime.now()
    dir_path = 'D:\\denva\\backup\\{}\\{:02d}\\{:02d}\\'.format(dt.year,dt.month,dt.day)
    logger.debug('performing information backup using path {}'.format(dir_path))
    Path(dir_path).mkdir(parents=True, exist_ok=True)
    dir_path +="information-backup." + utils.get_timestamp_file() + ".json"
    save_dict_data_as_json(dir_path,data)
