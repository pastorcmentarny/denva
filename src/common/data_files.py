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
from common import dom_utils
from denva import denva_sensors_service
from denviro import denviro_sensors_service
from services import email_sender_service
from zeroeighttrack import leaderboard_utils

logger = logging.getLogger('app')


def load_cfg() -> dict:
    if config_service.load_cfg()['mode'] == 'dev':
        path = 'd:\denva\email.json'
    elif config_service.load_cfg()['mode'] == 'server':
        path = 'e:\denva\email.json'
    else:
        path = '/home/pi/email.json'  # actual cfg is different place
    with open(path, 'r') as email_config:
        return json.load(email_config)


def save_report_at_server(report: dict):
    try:
        report_file_path = '{}/{}'.format(config_service.get_report_path_at_server(),
                                          dom_utils.get_date_as_filename('report', 'json',
                                                                         dom_utils.get_yesterday_date()))
        logger.info('Saving report to {}'.format(report_file_path))
        with open(report_file_path, 'w+', encoding='utf-8') as report_file:
            json.dump(report, report_file, ensure_ascii=False, indent=4)
    except Exception as e:
        logger.error('Unable to save report due to {}'.format(e))


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
        local_file = open(denviro_sensors_service.get_sensor_log_file(), 'a+', newline='')
        add_enviro_measurement_to_file(local_file, data)

        enviro_file = open(denviro_sensors_service.get_sensor_log_file_at_server(), 'a+', newline='')
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
                         dom_utils.get_float_number_from_text(data['cpu_temp']),
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
        local_file = open(denva_sensors_service.get_sensor_log_file(), 'a+', newline='')
        add_measurement_to_file(local_file, data, motion)

        server_file = open(denva_sensors_service.get_sensor_log_file_at_server(), 'a+', newline='')
        add_measurement_to_file(server_file, data, motion)

        logger.debug('measurement no.{} saved to file.'.format(counter))
    except IOError as exception:
        logger.warning(exception)


def setup_logging(where: str):
    path = config_service.get_environment_log_path_for(where)
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
    dir_path += "information-backup." + dom_utils.get_timestamp_file() + ".json"
    save_dict_data_as_json(dir_path, data)


def backup_results_data(results: list):
    dt = datetime.now()
    path = config_service.get_path_for_information_backup()
    dir_path = '{}backup\\{}\\{:02d}\\{:02d}\\'.format(path, dt.year, dt.month, dt.day)
    logger.debug('performing information backup using path {}'.format(dir_path))
    Path(dir_path).mkdir(parents=True, exist_ok=True)
    dir_path += "results-backup." + dom_utils.get_timestamp_file() + ".txt"
    eight_track_results = open(path, 'w', newline='')
    for result in results:
        eight_track_results.write(leaderboard_utils.convert_result_to_line(result))
        eight_track_results.write('\n')
    eight_track_results.close()


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


# TODO move this to different place
def load_data(year: int, month: int, day: int) -> list:
    sensor_log_file = dom_utils.fix_nulls(
        open(config_service.get_sensor_log_file_for(year, month, day), 'r', newline='', encoding='utf-8'))
    csv_content = csv.reader(sensor_log_file)
    csv_data = list(csv_content)
    data = []
    for row in csv_data:
        try:
            row[19] == '?'
        except IndexError:
            row.insert(19, '?')
            row.insert(20, '?')
        try:
            row[21] == '?'
        except IndexError:
            row.insert(21, '?')
            row.insert(22, '?')
        denva_sensors_service.add_row(data, row)
    sensor_log_file.close()
    return data


def load_enviro_data_for_today() -> list:
    today = datetime.now()
    return load_enviro_data(today.year, today.month, today.day)


def load_enviro_data(year: int, month: int, day: int) -> list:
    logger.debug('loading enviro sensor data from {} {} {}'.format(day, month, year))
    sensor_log_file = dom_utils.fix_nulls(
        open(config_service.get_sensor_log_file_for(year, month, day, 'sensor-enviro-log'), 'r', newline='',
             encoding='utf-8'))
    csv_content = csv.reader(sensor_log_file)
    csv_data = list(csv_content)
    data = []
    for index, row in enumerate(csv_data):
        logger.debug('read csv row no.{}'.format(index))
        try:
            row[12] == '?'
        except IndexError:
            row.insert(12, 0)  # measurement time
        denviro_sensors_service.add_enviro_row(data, row)
    sensor_log_file.close()
    return data


def is_report_file_exists() -> bool:
    report_file_path = '{}/{}'.format(config_service.get_report_path_at_server(),
                                      dom_utils.get_date_as_filename('report', 'json', dom_utils.get_yesterday_date()))
    return os.path.exists(report_file_path)
