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
import traceback
from datetime import date
from datetime import datetime
from pathlib import Path
from collections import Counter
from PIL import Image

import requests

# SETTINGS:
STORAGE_PATH = "/media/dom/PiSSD/cctv"
DEFAULT_TIMEOUT = 5
DARK = 8
WAIT_STEP = 0.1
RESOLUTION = '1920x1080'

logger = logging.getLogger('app')
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}

total_counter = 0
deleted = 0
ignored = 0
errors = 0


def get_date_with_time_as_filename(name: str, file_type: str, dt: datetime) -> str:
    return f"{name}-{dt.year}-{dt.month:02d}-{dt.day:02d}-{dt.hour:02d}{dt.minute:02d}{dt.second:02d}.{file_type}"


def get_date_as_folder():
    today = datetime.today()
    year = today.year
    month = today.month
    day = today.day
    hour = today.hour
    return "{}/{:02d}/{:02d}/{:02d}/".format(year, month, day, hour)


def capture_picture() -> str:
    try:
        start_time = time.perf_counter()
        date_as_folders = get_date_as_folder()
        path = Path("{}/{}".format(STORAGE_PATH, date_as_folders))
        if not path.exists():
            logger.warning(f'Path does not exists. Creating path {path}')
            Path(path).mkdir(parents=True, exist_ok=True)
        file = get_date_with_time_as_filename("cctv", "jpg", datetime.now())
        photo_path = str(Path('{}/{}'.format(path, file)))
        logger.debug('using path {}'.format(photo_path))

        # do picture using fswebcam
        try:
            p1 = subprocess.check_output(['fswebcam', '-r', RESOLUTION, '-S', '3', '--jpeg', '85,--save', photo_path],
                                         stderr=subprocess.PIPE, encoding='utf-8', bufsize=0, timeout=1)
            logger.debug(f"Output was : {p1}")
            time_out = 0
            while not os.path.exists(photo_path):
                time.sleep(WAIT_STEP)
                time_out += WAIT_STEP
                if time_out > 10:
                    logger.error(f"It looks file haven't been created with this path: {photo_path}")
                    break
                post_healthcheck_beat('knyszogar', 'cctv')
            logger.info('picture saved at {}'.format(photo_path))
        except subprocess.CalledProcessError as calledProcessError:
            logger.error(f"Subprocess throws error:{calledProcessError}")
            time.sleep(5)
        except Exception as exception:
            logger.error(f'Unable to do picture due to :{exception}')
            time.sleep(5)
        end_time = time.perf_counter()

        # TODO move to dom_utils
        total_time = str("%.2f" % (end_time - start_time))  # in ms
        logger.info('it took {} s to generate  and save a picture.'.format(total_time))
        return str(photo_path)
    except Exception as exception:
        logger.warning('Unable to capture picture due to {}'.format(exception), exc_info=True)
        # TODO email_sender_service.send_error_log_email("camera", "Unable to capture picture due to {}".format(calledProcessError))
    return ""


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


def is_photo_mostly_black(file, with_summary: bool = True):
    global total_counter
    global deleted
    global ignored
    global errors
    if os.path.splitext(file)[-1].lower() != ".jpg":
        logger.warning('{} is not a photo. Ignore it.'.format(file))
        ignored += 1
        return

    im = Image.open(file)  # Can be many formats.
    total_pixels = im.width * im.height
    pix = im.load()

    counter = []

    for x in range(0, im.width):
        for y in range(0, im.height):
            counter.append(pix[x, y])

    result = Counter(counter)
    dark_pixels = 0
    for d in result.items():
        if check_is_pixel_too_dark(d[0]):
            dark_pixels += d[1]
    too_dark = dark_pixels / total_pixels * 100
    if too_dark > 90:
        logger.info(file + 'is too dark and need to be deleted.')
        try:
            os.remove(file)
            if os.path.exists(file):
                logger.warning('{} NOT deleted.'.format(file))
            else:
                logger.info("{} deleted.".format(file))
                deleted += 1
        except Exception as e:
            logger.error('Unable to process {} file due to {}'.format(file, e))
            errors += 1
        print(f'Counter: {total_counter} with {deleted} deleted, {errors} errors and {ignored} ignored.')
    if with_summary:
        logger.info(str(dark_pixels) + ' out of ' + str(total_pixels) + ' is dark. (' + str(too_dark) + '%)')


def check_is_pixel_too_dark(pixel) -> bool:
    x, y, z = pixel
    return x <= DARK and y <= DARK and z <= DARK


def setup_test_logging(app_name: str):
    logging_level = logging.DEBUG
    logging_format = '%(levelname)s :: %(asctime)s :: %(message)s'
    logging_filename = f'/home/dom/data/logs/{app_name}-{date.today()}.txt'
    logging.basicConfig(level=logging_level, format=logging_format, filename=logging_filename)
    logging.captureWarnings(True)
    logging.debug('logging setup complete')


def app_loop():
    global total_counter
    while True:
        logger.info(f"Capturing picture no. {total_counter}")
        try:
            current_file = capture_picture()
            is_photo_mostly_black(current_file, False)
            total_counter += 1
            post_healthcheck_beat('knyszogar', 'cctv')
        except Exception as exception:
            logger.error(f"Something went wrong during capture/saving picture : {exception}", exc_info=True)
            traceback.print_exc()
            total_counter += 1


if __name__ == '__main__':
    setup_test_logging('cctv')
    app_loop()
