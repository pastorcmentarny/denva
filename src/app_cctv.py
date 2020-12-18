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
from datetime import datetime
from pathlib import Path
from time import sleep
from timeit import default_timer as timer

from picamera import PiCamera

import config_service
from common import data_files, app_timer
from common import dom_utils
from gateways import local_data_gateway
from services import email_sender_service
from tasks import too_dark_photos_remover_service

EMPTY = ''

logger = logging.getLogger('app')

camera = PiCamera()
WARM_UP_TIME = 1
email_cooldown = datetime.now()


def reset_camera():
    global camera
    camera.stop_preview()
    camera.close()
    sleep(WARM_UP_TIME)
    camera = PiCamera()


def capture_picture() -> str:
    global camera
    date_as_folders = dom_utils.get_date_as_folders_linux()
    path = Path("{}/{}".format("/home/pi/data/", date_as_folders))

    try:
        if not path.exists():
            logger.info('Path {} do not exist. Creating missing path.'.format(path))
            Path(path).mkdir(parents=True, exist_ok=True)

        file = dom_utils.get_date_with_time_as_filename("cctv", "jpg", datetime.now())

        photo_path = Path('{}/{}'.format(path, file))

        logger.debug('using path {}'.format(photo_path))

        camera.capture(str(photo_path))
        if too_dark_photos_remover_service.is_photo_mostly_black(photo_path, with_summary=False):
            logger.warning("Picture {} was too dark and it will be removed")
            os.remove(photo_path)
            if os.path.exists(photo_path):
                logger.warning('{} NOT deleted.'.format(photo_path))
            else:
                return EMPTY
        return photo_path
    except Exception as e:
        logger.warning('Unable to capture picture to {} due to {}'.format(path, e), exc_info=True)
        # email_sender_service.send_error_log_email("camera", "Unable to capture picture due to {}".format(e))
        # TODO sent error to status
        reset_camera()
    logger.warning('No path returned due to previous error.')
    return EMPTY


def main():
    global email_cooldown
    logger.info('Starting up camera')
    sleep(WARM_UP_TIME)

    camera.start_preview()
    camera.resolution = (640, 480)  # 3280x2464, 3280x2464,1920x1080,1640x1232, 1640x922,1280x720, 640x480
    logger.info('Camera is on.')

    measurement_counter = 0
    while config_service.is_sky_camera_on():
        measurement_counter += 1
        logger.info('Capturing photo no.{}'.format(measurement_counter))

        start_time = timer()
        last_picture = EMPTY
        captured_picture_path = capture_picture()
        if captured_picture_path != EMPTY:
            last_picture = captured_picture_path

        end_time = timer()
        measurement_time = int((end_time - start_time) * 1000)  # in ms

        remaining_time = 5 - (float(measurement_time) / 1000)
        if measurement_time > config_service.max_latency(fast=False):
            logger.warning("Measurement {} was slow. It took {} ms.".format(measurement_counter, measurement_time))
        else:
            logger.debug("It took {} ms.".format(measurement_time))

        if remaining_time > 0:
            time.sleep(remaining_time)

        if measurement_counter == 1 and last_picture != EMPTY:
            email_sender_service.send_picture(last_picture, measurement_counter)

        if app_timer.is_time_to_run_every_15_minutes(email_cooldown) and last_picture != EMPTY:
            email_sender_service.send_picture(last_picture, measurement_counter)
            email_cooldown = datetime.now()
        if measurement_counter % 2 == 0:
            local_data_gateway.post_healthcheck_beat('other', 'cctv')


if __name__ == '__main__':
    config_service.set_mode_to('cctv')
    data_files.setup_logging('cctv')
    logging.info('Starting application ...')
    email_sender_service.send_ip_email('CCTV APP')
    try:
        if config_service.is_sky_camera_on():
            main()
        else:
            logger.warning('Camera disabled.')
    except KeyboardInterrupt:
        logging.info('Received request application to shut down.. goodbye!', exc_info=True)
    except Exception as exception:
        print('Whoops. '.format(exception))
        logger.error('Something went badly wrong. {}'.format(exception), exc_info=True)
        email_sender_service.send_error_log_email("CCTV APP", "Application crashed due to {}.".format(exception))
