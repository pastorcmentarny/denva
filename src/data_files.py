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
import json
import logging
import logging.config
import os.path
import random
from datetime import datetime
from pathlib import Path

import config_service
import email_sender_service
import sensor_log_reader
import utils

logger = logging.getLogger('server')


def load_cfg() -> dict:
    if config_service.load_cfg()['mode'] == 'dev':
        path = 'd:\denva\email.json'
    elif config_service.load_cfg()['mode'] == 'server':
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


def add_enviro_measurement_to_file(file, data: dict):
    timestamp = datetime.now()
    csv_writer = csv.writer(file)
    csv_writer.writerow([timestamp,
                         data["temperature"], data["pressure"], data["humidity"],
                         data["light"], data["proximity"], data["oxidised"], data["reduced"],
                         data["nh3"], data["pm1"], data["pm25"], data["pm10"], data['measurement_time'],
                         data["cpu_temp"]
                         ])
    file.close()


# TODO refactor it as it saves in 2 places
def store_enviro_measurement(data: dict):
    try:
        local_file = open(sensor_log_reader.get_enviro_sensor_log_file(), 'a+', newline='')
        add_enviro_measurement_to_file(local_file, data)

        enviro_file = open(sensor_log_reader.get_enviro_sensor_log_file_at_server(), 'a+', newline='')
        add_enviro_measurement_to_file(enviro_file, data)
        # if flag is true, set to false
    except IOError as exception:
        logger.warning(exception)
        # add flag to indicate that there is a problem


def add_measurement_to_file(file, data: dict, motion):
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


# TODO refactor it as it saves in 2 places
# TODO merge motion with data
def store_measurement(data, motion):
    try:
        counter = data['measurement_counter']
    except Exception as exception:
        logger.warning(exception)
        counter = 0
    logger.debug('storing measurement no.{}'.format(counter))
    try:
        local_file = open(sensor_log_reader.get_sensor_log_file(), 'a+', newline='')
        add_measurement_to_file(local_file, data, motion)

        server_file = open(sensor_log_reader.get_sensor_log_file_at_server(), 'a+', newline='')
        add_measurement_to_file(server_file, data, motion)

        logger.debug('measurement no.{} saved to file.'.format(counter))
    except IOError as exception:
        logger.warning(exception)


def setup_logging():
    path = config_service.get_environment_log_path_for()
    if os.path.exists(path):
        with open(path, 'rt') as config_json_file:
            config = json.load(config_json_file)
        logging.config.dictConfig(config)
        logger.info('logs loaded from {}'.format(path))
    else:
        logging.basicConfig(level=logging.DEBUG)
        logger.warning('Using default logging due to problem with loading from log: {}'.format(path))
        email_sender_service.send_error_log_email(path,
                                                  'Unable to setup logging due to invalid path {}'.format(path))


def load_json_data_as_dict_from(path: str) -> dict:
    with open(path, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)


def save_dict_data_as_json(path: str, data: dict):
    with open(path, 'w', encoding='utf-8') as path_file:
        json.dump(data, path_file, ensure_ascii=False, indent=4)


def backup_information_data(data: dict):
    dt = datetime.now()
    path = config_service.get_path_for_information_backup()
    dir_path = '{}backup\\{}\\{:02d}\\{:02d}\\'.format(path, dt.year, dt.month, dt.day)
    logger.debug('performing information backup using path {}'.format(dir_path))
    Path(dir_path).mkdir(parents=True, exist_ok=True)
    dir_path += "information-backup." + utils.get_timestamp_file() + ".json"
    save_dict_data_as_json(dir_path, data)


# TODO improve convert files to files_list
def get_random_frame_picture_path():
    path = config_service.load_cfg()['paths']['frame'][config_service.get_mode()]
    files_list = []
    with os.scandir(path) as files:
        for file in files:
            files_list.append(path + "\\" + file.name)

    return files_list[random.randint(0, len(files_list) - 1)]


# TODO improve it, not my code. Do my own implementation and compare performance
def tail(file_path: str, lines=1) -> list:
    lines_found = []
    block_counter = -1
    file = open(file_path)
    while len(lines_found) < lines:
        try:
            file.seek(block_counter * 4098, os.SEEK_END)
        except IOError:
            file.seek(0)
            lines_found = file.readlines()
            break

        lines_found = file.readlines()
        block_counter -= 1

    return lines_found[-lines:]


def save_list_to_file(data: list, path: str):
    # TODO add validator?
    with open(path, 'w+', encoding='utf-8') as path_file:
        path_file.write('\n'.join(data))
    return None


def load_weather(path: str):
    with open(path, 'r', encoding='utf-8') as weather_file:
        return weather_file.read().splitlines()
