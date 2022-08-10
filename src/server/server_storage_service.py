import json
import logging
from retrying import retry

MODE = 'w'
ENCODING = 'utf-8'
logger = logging.getLogger('www')


def save_denva_measurement(data):
    __save(data, '/home/pi/data/denva_data.json')


def save_denviro_measurement(data):
    __save(data, '/home/pi/data/denviro_data.json')


def save_trases_measurement(data):
    __save(data, '/home/pi/data/trases_data.json')


def __retry_on_exception(exception):
    return isinstance(exception, Exception)


@retry(retry_on_exception=__retry_on_exception, wait_exponential_multiplier=50, wait_exponential_max=1000,
       stop_max_attempt_number=5)
def __save(data, path):
    try:
        with open(path, MODE, encoding=ENCODING) as trases_measurement_file:
            json.dump(data, trases_measurement_file, ensure_ascii=False, indent=4)
        return ""
    except Exception as exception:
        logger.error(f"Unable to save due to : {exception}", exc_info=True)
