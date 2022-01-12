import datetime
import json
import logging

import requests

logger = logging.getLogger('app')

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}


def post_healthcheck_beat(device: str, app_type: str):
    url = "http://192.168.0.205:5000/shc/update"
    json_data = {'device': device, 'app_type': app_type}
    try:
        with requests.post(url, json=json_data, timeout=2, headers=HEADERS) as response:
            response.json()
            response.raise_for_status()
    except Exception as whoops:
        logger.warning(
            'There was a problem: {} using url {}, device {} and app_type {}'.format(whoops, url, device, app_type))


def setup_test_logging(app_name: str):
    logging_level = logging.INFO
    logging_format = '%(levelname)s :: %(asctime)s :: %(message)s'
    logging_filename = f'log-{app_name}-{datetime.date.today()}.txt'
    logging.basicConfig(level=logging_level, format=logging_format, filename=logging_filename)
    logging.captureWarnings(True)
    logging.debug('logging setup complete')


def load_cfg() -> dict:
    with open('/home/pi/email.json', 'r') as email_config:
        return json.load(email_config)
