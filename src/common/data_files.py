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
import logging.config as log_config
import os.path
import random
from datetime import datetime, date

import config
import dom_utils

from common import data_loader, data_writer
from common.gobshite_exception import GobshiteException

logger = logging.getLogger('app')


def load_weather(path: str):
    logger.debug(f'Loading weather data from {path}')
    return data_loader.load_weather(path)


def load_report(report_date: str) -> dict:
    report_file_path = f'{config.get_report_path()}/{report_date}'
    logger.info(f'Loading report from {report_file_path}')
    return data_loader.load_json_data_as_dict_from(report_file_path)


def load_warnings(warning_path: str) -> list:
    logger.info(f'Loading warning from {warning_path}')
    content = data_loader.load_as_list_from_file(warning_path)
    content.insert(0, f'Warning counts: {len(content)}')
    return content


def load_email_config() -> dict:
    return data_loader.load_json_data_as_dict_from(config.get_email_config_path())


def load_network_health_check_results():
    result = data_loader.load_json_data_as_dict_from("data/nhc.json")
    if 'error' in result:
        logger.warning(f'loading network hc file failed due to {result["error"]}')
        return {
            "status": config.UNKNOWN,
            "result": "Unable to load file",
            "problems": [result['error']]
        }
    else:
        return result


def load_ricky(path: str):
    return data_loader.load_json_data_as_dict_from(path)


# TODO move generated metrics path to config
def save_metrics(stats: dict, path):
    full_path = path + f'metrics-{str(stats["date"])}.txt'
    data_writer.save_dict_data_as_json(full_path, stats)


# TODO move generated metrics path to config
def load_metrics_data(path: str) -> dict:
    metric_data_file = f'metrics-{str(date.today())}.txt'
    path = path + metric_data_file
    try:
        return data_loader.load_json_data_as_dict_from(path)
    except Exception as exception:
        logging.warning(f'Unable to load metrics data ${metric_data_file} to file due to: ${exception}', exc_info=True)
        return {}


def load_stats(stats_path: str) -> list:
    logger.info(f'Loading stats from {stats_path}')
    return data_loader.load_as_list_from_file(stats_path)


def load_last_measurement_for(device):
    return data_loader.__load(f'/home/ds/data/{device}_data.json')


def store_last_100_measurement(measurement_counter, measurements_list, file_name):
    if measurement_counter % 100 == 0:
        store_measurement2(dom_utils.get_today_date_as_filename(file_name, 'txt'),
                           measurements_list[-100:])


def save_report(report: dict, file: str):
    report_file_path = f'{config.get_report_path()}/{file}'
    logger.info(f'Saving report to {report_file_path}')
    data_writer.save_dict_data_as_json(report_file_path, report)


def save_warnings(warnings: list):
    today_warnings_path = f"{config.PI_DATA_PATH}{dom_utils.get_date_as_folders()}warnings.txt"
    data_writer.save_list_to_file(warnings, today_warnings_path, config.APPEND_WITH_READ_MODE)


# TODO merge with store_measurement2
def store_measurement(data, sensor_log_file):
    row = [datetime.now(),
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
           data[config.FIELD_UVA],
           data[config.FIELD_UVB],
           data[config.FIELD_UV]
           ]
    data_writer.store_measurement(row, sensor_log_file, data[config.FIELD_MEASUREMENT_COUNTER])


# TODO merge with store_measurement
def store_measurement2(sensor_data: str, measurements: list):
    data_writer.store_measurement2(sensor_data, measurements)


def check_if_report_was_generated(report_date: str) -> bool:
    path = f'{config.get_report_path()}/{report_date}'
    return os.path.isfile(path)


def setup_logging(path: str):
    if os.path.exists(path):
        config_data = data_loader.load_json_data_as_dict_from(path)
        log_config.dictConfig(config_data)
        logging.captureWarnings(True)
        logger.info(f'logs loaded from {path}')
    else:
        logging.basicConfig(level=logging.DEBUG)
        logging.captureWarnings(True)
        logger.warning(f'Using default logging due to problem with loading from log: {path}')


def backup_information_data(data: dict):
    logger.info(f'Creating a backup for information data ... ')
    dir_path = data_writer.create_backup_dir_path_for("information-backup.", ".json", config.PI_HOME_DIR)
    logger.info(f' ... using path: {dir_path}')
    data_writer.save_dict_data_as_json(dir_path, data)


def get_random_frame_picture_path(path: str):
    if not os.path.exists(path):
        raise GobshiteException(f'Setup messed up, No dir found for {path}')
    files_list = []
    with os.scandir(path) as files:
        for file in files:
            files_list.append(path + "\\" + file.name)

    return files_list[random.randint(0, len(files_list) - 1)]


def tail(file_path: str, lines=1) -> list:  # not my code
    return data_loader.tail(file_path, lines)


def is_report_file_exists(path) -> bool:
    report_file_path = f"{path}/{dom_utils.get_date_as_filename('report', 'json', dom_utils.get_yesterday_datetime())}"
    return os.path.exists(report_file_path)


def count_lines(path):
    counter = 0
    try:
        with open(path, config.READ_MODE) as fp:
            for _ in enumerate(fp):
                counter += 1
    except Exception as exception:
        logging.warning(f'Unable to warning file due to: ${exception}', exc_info=True)
        return 0


def load_logs(path):
    with open(path, config.READ_MODE, encoding=config.ENCODING) as logs_file:
        return logs_file.read().splitlines()


def save_entry(new_entry, path):
    data_writer.add_new_line_of_text_to_file(new_entry, path)
