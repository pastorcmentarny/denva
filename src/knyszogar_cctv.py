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

import logging
import os
import time
from datetime import datetime, date
from pathlib import Path

import utils

logger = logging.getLogger('app')
step = 0.1
resolution = '1280x720'


# FIXME use
def get_date_as_folders_linux(specified_data: date):
    today = specified_data
    year = today.year
    month = today.month
    day = today.day
    return "{}/{:02d}/{:02d}/".format(year, month, day)


def get_date_with_time_as_filename(name: str, file_type: str, dt: datetime) -> str:
    return f"{name}-{dt.year}-{dt.month:02d}-{dt.day:02d}-{dt.hour:02d}{dt.minute:02d}{dt.second:02d}.{file_type}"


def capture_picture() -> str:
    try:
        start_time = time.perf_counter()

        date_as_folders = get_date_as_folders_linux(date.today())
        path = Path("{}/{}".format("/home/pi/sky", date_as_folders))
        if not path.exists():
            print(f'Path does not exists. Creating path {path}')
            Path(path).mkdir(parents=True, exist_ok=True)
        file = get_date_with_time_as_filename("cctv", "jpg", datetime.now())
        photo_path = str(Path('{}/{}'.format(path, file)))
        logger.info('using path {}'.format(photo_path))

        # do picture using fswebcam
        os.system(f'''timeout 5s fswebcam -r {resolution} -S 3 --jpeg 85 --save {photo_path}''')

        while not os.path.exists(photo_path):
            time.sleep(step)
        logger.info('picture saved at {}'.format(photo_path))
        end_time = time.perf_counter()

        total_time = str("%.2f" % (end_time - start_time))  # in ms
        logger.info('it took {} s to generate  and save a picture.'.format(total_time))
        return str(photo_path)
    except Exception as exception:
        logger.warning('Unable to capture picture due to {}'.format(exception), exc_info=True)
        # TODO email_sender_service.send_error_log_email("camera", "Unable to capture picture due to {}".format(e))
    return ""


def app_loop():
    counter = 0
    while True:
        logger.info(f"Capturing picture no. {counter}")
        capture_picture()
        counter += 1
        utils.post_healthcheck_beat('knyszogar', 'cctv')
        time.sleep(4.2)


if __name__ == '__main__':
    utils.setup_test_logging('cctv')
    app_loop()
