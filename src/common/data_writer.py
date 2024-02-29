import json

from retrying import retry
import logging
import csv
import config
from pathlib import Path
from datetime import datetime

import dom_utils

logger = logging.getLogger('app')


def __retry_on_exception(exception):
    logger.warning('Retrying failed operation...')
    return isinstance(exception, Exception)


def save_list_to_file(data: list, path: str, file_mode: str == config.APPEND_WITH_READ_MODE):
    try:
        filename = Path(path)
        filename.touch(exist_ok=True)
        with open(path, file_mode, encoding=config.ENCODING) as path_file:
            path_file.write(config.NEW_LINE.join(data))
            path_file.write(config.NEW_LINE)
    except Exception as exception:
        logger.warning(f"Unable to save this data {data} using path {path} due to {exception}")


def save_list_to_file_replace(data: list, path: str):
    save_list_to_file(data, path, config.WRITE_MODE)


def save_dict_data_to_file(data: dict, file_name):
    file_path = f'{config.PI_DATA_PATH}{file_name}.txt'
    try:
        logger.debug(f'Saving dictionary of size {len(data)} to {file_path}')
        with open(file_path, config.WRITE_WITH_READ_MODE, encoding=config.ENCODING) as report_file:
            report_file.write(json.dumps(data, ensure_ascii=False))
    except Exception as save_data_exception:
        logger.error(f'Unable to save  due to {save_data_exception}', exc_info=True)


@retry(retry_on_exception=__retry_on_exception, wait_exponential_multiplier=50, wait_exponential_max=1000,
       stop_max_attempt_number=5)
def save_dict_data_as_json(path: str, file_data: dict):
    try:
        with open(path, config.WRITE_WITH_READ_MODE, encoding=config.ENCODING) as path_file:
            json.dump(file_data, path_file, ensure_ascii=False, indent=4)
    except Exception as exception:
        logger.warning(f'Unable to save this data {file_data} due to {exception}')


def store_measurement(row, sensor_log_file, counter):
    logger.debug(f'Storing measurement no.{counter}')
    try:
        with open(sensor_log_file, config.APPEND_WITH_READ_MODE, newline=config.EMPTY) as local_file:
            logger.debug(f'adding measurement to {local_file}')
            csv_writer = csv.writer(local_file)
            csv_writer.writerow(row)

            logger.debug(f'Measurement no.{counter} saved to file.')
    except IOError as exception:
        logger.warning(f'Unable to store denvira measurement due to : {exception}', exc_info=True)


def store_measurement2(sensor_data: str, measurements: list):
    sensor_log_file = f"/home/ds/data/{sensor_data}"
    logger.debug(f'Storing measurement to {sensor_log_file}')
    try:
        with open(sensor_log_file, config.APPEND_WITH_READ_MODE, newline=config.EMPTY,
                  encoding=config.ENCODING) as report_file:
            for measurement in measurements:
                report_file.write(f'{json.dumps(measurement, ensure_ascii=False)}\n')
        logger.debug(f'Measurement stored to {sensor_log_file}')
    except IOError as io_exception:
        logger.error(io_exception, exc_info=True)


def create_backup_dir_path_for(dir_name: str, suffix: str, path: str):
    dt = datetime.now()
    dir_path = f'{path}backup/{dt.year}/{dt.month:02d}/{dt.day:02d}/'
    logger.debug(f'Performing information backup using path {dir_path}')
    Path(dir_path).mkdir(parents=True, exist_ok=True)
    dir_path += dir_name + dom_utils.get_timestamp_file() + suffix
    return dir_path


def add_new_line_of_text_to_file(new_entry: str, path: str):
    try:
        with open(path, config.APPEND_WITH_READ_MODE, encoding=config.ENCODING) as diary_file:
            diary_file.write(new_entry)
            diary_file.write(config.NEW_LINE)
    except IOError as io_exception:
        logger.error(f'Failed to save {new_entry} to file {path} due to {io_exception}')