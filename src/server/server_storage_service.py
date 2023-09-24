import json
import logging
from retrying import retry

READ = 'r'
MODE = 'w'
ENCODING = 'utf-8'
logger = logging.getLogger('app')


def save_denva_measurement(data):
    __save(data, '/home/pi/data/denva_data.json')


def __retry_on_exception(exception):
    return isinstance(exception, Exception)


@retry(retry_on_exception=__retry_on_exception, wait_exponential_multiplier=50, wait_exponential_max=1000,
       stop_max_attempt_number=5)
def __save(data, path):
    try:
        with open(path, MODE, encoding=ENCODING) as measurement_file:
            json.dump(data, measurement_file, ensure_ascii=False, indent=4)
        return ""
    except Exception as exception:
        logger.error(f"Unable to save due to : {exception}", exc_info=True)
