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
import csv
import json
import logging
import logging.config
import os.path
import random
from datetime import datetime, date
from pathlib import Path

import config
import dom_utils
from retrying import retry

EMPTY = ''

READ = 'r'

ENCODING = 'utf-8'
UNKNOWN = '?'

logger = logging.getLogger('app')

report_dir = '/home/pi/reports'


def load_cfg() -> dict:
    with open('/home/pi/email.json', READ) as email_config:
        return json.load(email_config)


def save_report_at_server(report: dict, report_path):
    try:
        report_file_path = '{}/{}'.format(report_path,
                                          dom_utils.get_date_as_filename('report', 'json',
                                                                         dom_utils.get_yesterday_date()))
        logger.info('Saving report to {}'.format(report_file_path))
        with open(report_file_path, 'w+', encoding=ENCODING) as report_file:
            json.dump(report, report_file, ensure_ascii=False, indent=4)
    except Exception as exception:
        logger.error('Unable to save report due to {}'.format(exception))


def save_report(report: dict, file: str):
    report_file_path = '{}/{}'.format(report_dir, file)
    logger.info('Saving report to {}'.format(report_file_path))
    with open(report_file_path, 'w+', encoding=ENCODING) as report_file:
        json.dump(report, report_file, ensure_ascii=False, indent=4)


# report on Pi
def load_report(report_date: str) -> dict:
    report_file_path = '{}/{}'.format(report_dir, report_date)
    logger.info('Loading report from {}'.format(report_file_path))
    with open(report_file_path, READ) as report_file:
        return json.load(report_file)


def load_report_on_server_on(report_date: datetime, report_path: str):
    report_file_path = '{}/{}'.format(report_path,
                                      dom_utils.get_date_as_filename('report', 'json',
                                                                     report_date))
    logger.info('Loading report from {}'.format(report_file_path))
    with open(report_file_path, READ) as report_file:
        return json.load(report_file)


def load_warnings(path: str) -> list:
    file = open(path, READ, newline=EMPTY)
    content = file.readlines()
    content.insert(0, 'Warning counts: {}'.format(len(content)))
    return content


def load_stats(path: str) -> list:
    file = open(path, READ, newline=EMPTY)
    content = file.readlines()
    return content


def check_if_report_was_generated(report_date: str) -> bool:
    path = '{}/{}'.format(report_dir, report_date)
    return os.path.isfile(path)


def add_enviro_measurement_to_file(file, data: dict):
    timestamp = datetime.now()
    csv_writer = csv.writer(file)
    csv_writer.writerow([timestamp,
                         data[config.FIELD_TEMPERATURE], data[config.FIELD_PRESSURE], data[config.FIELD_HUMIDITY],
                         data[config.FIELD_LIGHT], data[config.FIELD_PROXIMITY], data[config.FIELD_OXIDISED],
                         data[config.FIELD_REDUCED],
                         data[config.FIELD_NH3], data[config.FIELD_PM1], data[config.FIELD_PM25],
                         data[config.FIELD_PM10], data[config.FIELD_MEASUREMENT_TIME],
                         data[config.FIELD_CPU_TEMP]
                         ])
    file.close()


def store_enviro_measurement(data: dict, sensor_log_file):
    try:
        local_file = open(sensor_log_file, 'a+', newline=EMPTY)
        add_enviro_measurement_to_file(local_file, data)
    except IOError as exception:
        logger.warning(f'Unable to store denvira measurement due to : {exception}', exc_info=True)


def add_measurement_to_file(file, data: dict):
    timestamp = datetime.now()
    csv_writer = csv.writer(file)
    csv_writer.writerow([timestamp,
                         data[config.FIELD_MEASUREMENT_TIME],
                         data[config.FIELD_TEMPERATURE],
                         data[config.FIELD_PRESSURE],
                         data[config.FIELD_HUMIDITY],
                         data[config.FIELD_GAS_RESISTANCE],
                         data[config.FIELD_COLOUR],
                         data[config.FIELD_RED],
                         data[config.FIELD_GREEN],
                         data[config.FIELD_BLUE],
                         data[config.FIELD_CO2],
                         data[config.FIELD_CO2_TEMPERATURE],
                         data[config.FIELD_RELATIVE_HUMIDITY],
                         dom_utils.get_float_number_from_text(data[config.FIELD_CPU_TEMP]),
                         data[config.FIELD_ECO2],
                         data[config.FIELD_TVOC],
                         data[config.FIELD_GPS_LATITUDE],
                         data[config.FIELD_GPS_LONGITUDE],
                         data[config.FIELD_GPS_ALTITUDE],
                         data[config.FIELD_GPS_LAT_DIR], data[config.FIELD_GPS_LON_DIR],
                         data[config.FIELD_GPS_GEO_SEP], data[config.FIELD_GPS_NUM_SATS], data[config.FIELD_GPS_QUAL],
                         data[config.FIELD_GPS_SPEED_OVER_GROUND],
                         data[config.FIELD_GPS_MODE_FIX_TYPE], data[config.FIELD_GPS_PDOP], data[config.FIELD_GPS_HDOP],
                         data[config.FIELD_GPS_VDOP]
                         ])
    file.close()


def store_measurement(data, sensor_log_file):
    try:
        counter = data[config.FIELD_MEASUREMENT_COUNTER]
    except Exception as exception:
        logger.warning(f'Unable to store denva measurement due to : {exception}', exc_info=True)
        counter = 0
    logger.debug('Storing measurement no.{}'.format(counter))
    try:
        local_file = open(sensor_log_file, 'a+', newline=EMPTY)
        add_measurement_to_file(local_file, data)

        logger.debug('Measurement no.{} saved to file.'.format(counter))
    except IOError as exception:
        logger.warning(f'Unable to store denvira measurement due to : {exception}', exc_info=True)


def setup_logging(path: str):
    if os.path.exists(path):
        with open(path, 'rt') as config_json_file:
            config = json.load(config_json_file)
        logging.config.dictConfig(config)
        logging.captureWarnings(True)
        logger.info('logs loaded from {}'.format(path))
    else:
        logging.basicConfig(level=logging.DEBUG)
        logging.captureWarnings(True)
        logger.warning('Using default logging due to problem with loading from log: {}'.format(path))


def load_json_data_as_dict_from(path: str) -> dict:
    with open(path, READ, encoding=ENCODING) as json_file:
        return json.load(json_file)


def save_dict_data_as_json(path: str, data: dict):
    try:
        with open(path, "w+", encoding=ENCODING) as path_file:
            json.dump(data, path_file, ensure_ascii=False, indent=4)
    except Exception as exception:
        logger.warning(f"Unable to save this data {data} due to {exception}")


def backup_information_data(data: dict):
    dir_path = create_backup_dir_path_for("information-backup.", ".json", config.PI_HOME_DIR)
    save_dict_data_as_json(dir_path, data)


def create_backup_dir_path_for(dir_name: str, suffix: str, path: str):
    dt = datetime.now()
    dir_path = '{}backup\\{}\\{:02d}\\{:02d}\\'.format(path, dt.year, dt.month, dt.day)
    logger.debug('performing information backup using path {}'.format(dir_path))
    Path(dir_path).mkdir(parents=True, exist_ok=True)
    dir_path += dir_name + dom_utils.get_timestamp_file() + suffix
    return dir_path


# TODO improve convert files to files_list
def get_random_frame_picture_path(path: str):
    files_list = []
    with os.scandir(path) as files:
        for file in files:
            files_list.append(path + "\\" + file.name)

    return files_list[random.randint(0, len(files_list) - 1)]


# TODO improve it, not my code. Do my own implementation and compare performance
def tail(file_path: str, lines=1) -> list:
    lines_found = []
    block_counter = -1
    with open(file_path) as file:
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


# TODO add validator? and RETRY
def save_list_to_file(data: list, path: str):
    try:
        filename = Path(path)
        filename.touch(exist_ok=True)
        with open(path, 'a+', encoding=ENCODING) as path_file:
            path_file.write('\n'.join(data))
            path_file.write('\n')
    except Exception as exception:
        logger.warning(f"Unable to save this data {data} using path {path} due to {exception}")


def load_weather(path: str):
    with open(path, READ, encoding=ENCODING) as weather_file:
        return weather_file.read().splitlines()


# TODO move this to different place
def load_data(path: str) -> list:
    sensor_log_file = dom_utils.fix_nulls(
        open(path, READ, newline=EMPTY, encoding=ENCODING))
    csv_content = csv.reader(sensor_log_file)
    csv_data = list(csv_content)
    data = []
    for row in csv_data:
        add_denva_row(data, row)
    sensor_log_file.close()
    return data


def add_denva_row(data, row):
    data.append(
        {
            config.FIELD_TIMESTAMP: row[config.DENVA_DATA_COLUMN_TIMESTAMP],
            config.FIELD_TEMPERATURE: row[config.DENVA_DATA_COLUMN_TEMP],
            config.FIELD_PRESSURE: row[config.DENVA_DATA_COLUMN_PRESSURE],
            config.FIELD_HUMIDITY: row[config.DENVA_DATA_COLUMN_HUMIDITY],
            config.FIELD_RELATIVE_HUMIDITY: row[config.DENVA_DATA_COLUMN_RELATIVE_HUMIDITY],
            config.FIELD_GAS_RESISTANCE: row[config.DENVA_DATA_COLUMN_GAS_RESISTANCE],
            config.FIELD_CO2: row[config.DENVA_DATA_COLUMN_CO2],
            config.FIELD_CO2_TEMPERATURE: row[config.DENVA_DATA_COLUMN_CO2_TEMPERATURE],
            config.FIELD_MEASUREMENT_TIME: row[config.DENVA_DATA_COLUMN_MEASUREMENT_TIME],
            config.FIELD_CPU_TEMP: row[config.DENVA_DATA_COLUMN_CPU_TEMP],
            config.FIELD_ECO2: row[config.DENVA_DATA_COLUMN_ECO2],
            config.FIELD_TVOC: row[config.DENVA_DATA_COLUMN_TVOC],
            config.FIELD_GPS_NUM_SATS: row[config.DENVA_DATA_COLUMN_GPS_NUM_SATS],
        }
    )


def load_enviro_data_for_today() -> list:
    today = datetime.now()
    return load_enviro_data(today.year, today.month, today.day, get_sensor_log_file())


def get_sensor_log_file():
    return config.PI_DATA_PATH + dom_utils.get_date_as_filename('sensor-log', 'csv', datetime.now())


def load_enviro_data(year: int, month: int, day: int, path: str) -> list:
    logger.debug('loading enviro sensor data from {} {} {}'.format(day, month, year))
    sensor_log_file = dom_utils.fix_nulls(
        open(path, READ, newline=EMPTY,
             encoding=ENCODING))
    csv_content = csv.reader(sensor_log_file)
    csv_data = list(csv_content)
    data = []
    for index, row in enumerate(csv_data):
        logger.debug('read csv row no.{}'.format(index))
        try:
            row[12] == UNKNOWN
        except IndexError:
            row.insert(12, 0)  # measurement time
        add_enviro_row(data, row)
    sensor_log_file.close()
    return data


def add_enviro_row(data, row):
    data.append(
        {
            config.FIELD_TIMESTAMP: row[0],
            config.FIELD_TEMPERATURE: '{:0.1f}'.format(float(row[1])),  # unit = "C"
            config.FIELD_OXIDISED: '{:0.2f}'.format(float(row[6])),  # config.FIELD_OXIDISED    unit = "kO"
            config.FIELD_REDUCED: '{:0.2f}'.format(float(row[7])),  # unit = "kO"
            config.FIELD_NH3: '{:0.2f}'.format(float(row[8])),  # unit = "kO"
            config.FIELD_PM1: row[9],  # unit = "ug/m3"
            config.FIELD_PM25: row[10],  # unit = "ug/m3"
            config.FIELD_PM10: row[11],  # unit = "ug/m3"
            config.FIELD_CPU_TEMP: row[13],
            config.FIELD_LIGHT: '{:0.1f}'.format(float(row[4])),
            config.FIELD_MEASUREMENT_TIME: row[12]
        }
    )


def is_report_file_exists(path) -> bool:
    report_file_path = '{}/{}'.format(path,
                                      dom_utils.get_date_as_filename('report', 'json', dom_utils.get_yesterday_date()))
    return os.path.exists(report_file_path)


def is_report_file_exists_for(report_date: datetime, path: str) -> bool:
    report_file_path = '{}/{}'.format(path,
                                      dom_utils.get_date_as_filename('report', 'json', report_date))
    return os.path.exists(report_file_path)


def load_ricky(path: str):
    with open(path, READ, encoding=ENCODING) as ricky_data:
        return json.load(ricky_data)


def load_text_to_display(path) -> str:
    try:
        with open(path, READ, encoding=ENCODING) as text_file:
            return str(text_file.read())
    except Exception as exception:
        logging.warning(f'Unable to load file with message due to: ${exception}', exc_info=True)
        return str(exception)


def save_metrics(stats: dict, path) -> str:
    try:
        full_path = path + f'metrics-{str(stats["date"])}.txt'
        save_dict_data_as_json(full_path, stats)
        return 'saved'
    except Exception as exception:
        logging.warning(f'Unable to save stats ${stats} to file due to: ${exception}', exc_info=True)
        return str(exception)


def load_metrics_data(path: str) -> dict:
    metric_data_file = f'metrics-{str(date.today())}.txt'
    path = path + metric_data_file
    try:
        return load_json_data_as_dict_from(path)
    except Exception as exception:
        logging.warning(f'Unable to load metrics data ${metric_data_file} to file due to: ${exception}', exc_info=True)
        return {}


def __retry_on_exception(exception):
    return isinstance(exception, Exception)


@retry(retry_on_exception=__retry_on_exception, wait_exponential_multiplier=50, wait_exponential_max=1000,
       stop_max_attempt_number=5)
def __load(path: str) -> dict:
    with open(path, READ, encoding=ENCODING) as json_file:
        return json.load(json_file)


def load_last_measurement_for(device):
    return __load(f'/home/pi/data/{device}_data.json')


def save_warnings(warnings: list):
    today_warnings_path = f"{config.PI_DATA_PATH}{dom_utils.get_date_as_folders()}warnings.txt"
    save_list_to_file(warnings, today_warnings_path)
