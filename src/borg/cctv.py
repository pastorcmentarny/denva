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
import os
import subprocess
import time
from datetime import date
from datetime import datetime
from pathlib import Path

import requests

DEFAULT_TIMEOUT = 5
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}

logger = logging.getLogger('app')
step = 0.1
resolution = '1280x720'


def get_date_with_time_as_filename(name: str, file_type: str, dt: datetime) -> str:
    return f"{name}-{dt.year}-{dt.month:02d}-{dt.day:02d}-{dt.hour:02d}{dt.minute:02d}{dt.second:02d}.{file_type}"


def get_date_as_folder():
    today = date.today()
    year = today.year
    month = today.month
    day = today.day
    return "{}/{:02d}/{:02d}/".format(year, month, day)


def capture_picture() -> str:
    try:
        start_time = time.perf_counter()
        date_as_folders = get_date_as_folder()
        path = Path("{}/{}".format("/home/dom/data/cctv", date_as_folders))
        if not path.exists():
            logger.warning(f'Path does not exists. Creating path {path}')
            Path(path).mkdir(parents=True, exist_ok=True)
        file = get_date_with_time_as_filename("cctv", "jpg", datetime.now())
        photo_path = str(Path('{}/{}'.format(path, file)))
        logger.debug('using path {}'.format(photo_path))

        # do picture using fswebcam
        try:
            p1 = subprocess.check_output(['fswebcam', '-r', resolution, '-S', '3', '--jpeg', '85,--save', photo_path],
                                         stderr=subprocess.PIPE, encoding='utf-8', bufsize=0)
            try:
                output_data, error_output_data = p1.communicate(
                    timeout=1)  # will raise error and kill any process that runs longer than 60 seconds
                logger.debug(output_data)
                print(output_data)
                logger.error(error_output_data)
                print(error_output_data)
                post_healthcheck_beat('knyszogar', 'cctv')
            except Exception as exception:
                logger.error(f'unable to do picture due to {exception}')
                p1.kill()
                print('Waiting 30 seconds before capture picture again')
                time.sleep(30)

            while not os.path.exists(photo_path):
                time.sleep(step)
            logger.info('picture saved at {}'.format(photo_path))
        except subprocess.CalledProcessError as calledProcessError:
            logger.error(f"Subprocess throws error:{calledProcessError}")
        except Exception as exception:
            logger.error(f'Unable to do picture due to :{exception}')

        end_time = time.perf_counter()

        # TODO move to dom_utils
        total_time = str("%.2f" % (end_time - start_time))  # in ms
        logger.info('it took {} s to generate  and save a picture.'.format(total_time))
        return str(photo_path)
    except Exception as exception:
        logger.warning('Unable to capture picture due to {}'.format(exception), exc_info=True)
        # TODO email_sender_service.send_error_log_email("camera", "Unable to capture picture due to {}".format(calledProcessError))
    return ""


def app_loop():
    counter = 0
    while True:
        logger.info(f"Capturing picture no. {counter}")
        capture_picture()
        counter += 1
        post_healthcheck_beat('knyszogar', 'cctv')
        time.sleep(2.5)


def post_healthcheck_beat(device: str, app_type: str):
    url = "http://192.168.0.200:5000/shc/update"
    json_data = {'device': device, 'app_type': app_type}
    try:
        with requests.post(url, json=json_data, timeout=2, headers=HEADERS) as response:
            response.json()
            response.raise_for_status()
    except Exception as whoops:
        logger.warning(
            'There was a problem: {} using url {}, device {} and app_type {}'.format(whoops, url, device, app_type))


def setup_test_logging(app_name: str):
    logging_level = logging.DEBUG
    logging_format = '%(levelname)s :: %(asctime)s :: %(message)s'
    logging_filename = f'/home/dom/data/logs/{app_name}-{date.today()}.txt'
    logging.basicConfig(level=logging_level, format=logging_format, filename=logging_filename)
    logging.captureWarnings(True)
    logging.debug('logging setup complete')


if __name__ == '__main__':
    setup_test_logging('cctv')
    app_loop()
