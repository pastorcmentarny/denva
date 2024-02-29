import os

from retrying import retry
import logging
import config
import json
import csv

import dom_utils

logger = logging.getLogger('app')


def __retry_on_exception(exception):
    logger.warning('Retrying failed operation...')
    return isinstance(exception, Exception)


@retry(retry_on_exception=__retry_on_exception, wait_exponential_multiplier=50, wait_exponential_max=1000,
       stop_max_attempt_number=5)
def load_json_data_as_dict_from(path: str) -> dict:
    try:
        with open(path, config.READ_MODE, encoding=config.ENCODING) as json_file:
            return json.load(json_file)
    except Exception as exception:
        msg = f"Unable to load this file {path} due to {exception}"
        logger.warning(msg, exc_info=True)
        return {'error': msg}


@retry(retry_on_exception=__retry_on_exception, wait_exponential_multiplier=50, wait_exponential_max=1000,
       stop_max_attempt_number=5)
def load_weather(path: str):
    with open(path, config.READ_MODE, encoding=config.ENCODING) as weather_file:
        return weather_file.read().splitlines()


@retry(retry_on_exception=__retry_on_exception, wait_exponential_multiplier=50, wait_exponential_max=1000,
       stop_max_attempt_number=5)
def load_data_as_list_from_csv(path: str) -> list:
    try:
        with open(path, config.READ_MODE, newline=config.EMPTY, encoding=config.ENCODING) as sensor_log_file:
            sensor_log_file = dom_utils.fix_nulls(sensor_log_file)
            csv_content = csv.reader(sensor_log_file)
            return list(csv_content)
    except Exception as exception:
        logger.error(f'Unable to load processed reading due to {exception}', exc_info=True)
        return []


@retry(retry_on_exception=__retry_on_exception, wait_exponential_multiplier=50, wait_exponential_max=1000,
       stop_max_attempt_number=5)
def load_as_list_from_file(file_path: str):
    if os.path.isfile(file_path):
        try:
            with open(file_path, config.READ_MODE, encoding=config.ENCODING, newline=config.NEW_LINE) as data_file:
                return data_file.readlines()
        except Exception as load_data_exception:
            logger.error(f'Unable to load data from {file_path}  due to {load_data_exception}', exc_info=True)
            return []
    else:
        logger.error(f'File {file_path} does NOT exists.')
        return []


@retry(retry_on_exception=__retry_on_exception, wait_exponential_multiplier=50, wait_exponential_max=1000,
       stop_max_attempt_number=5)
def __load(path: str) -> dict:
    try:
        with open(path, config.READ_MODE, encoding=config.ENCODING) as json_file:
            return json.load(json_file)
    except Exception as exception:
        logging.warning(f'Unable to load data from ${path} due to: ${exception}', exc_info=True)
    return {}


def load_list_of_dict_for(path_to_file: str):
    logger.debug(f'loading list with path {path_to_file}')
    data_as_dict_list = []
    with open(path_to_file, config.READ_MODE, encoding=config.ENCODING) as data_file:
        content_list = data_file.readlines()
        for item in content_list:
            if item.strip() != config.EMPTY and len(item.strip()) > 2:
                data_as_dict_list.append(json.loads(item.strip()))
    logger.debug('task done')
    return data_as_dict_list


def tail(file_path: str, lines=1) -> list:  # not my code
    lines_found = []
    block_counter = -1
    try:
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
    except Exception as exception:
        logger.error(f'Something went badly wrong due to {exception}', exc_info=True)
        return []
