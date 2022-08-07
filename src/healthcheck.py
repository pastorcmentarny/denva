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
import config
import logging
import time
import traceback
from datetime import datetime

import requests

from common import data_files, commands
import dom_utils
from denva import denva_sensors_service
from emails import email_sender_service

logger = logging.getLogger('hc')

"""
Healthcheck checks:
 - is app is running
 - when last measurement was
 - check when last photo was taken
if something wrong restart and send email
"""

attempts = 5
wait_time = 30
reasons = []


def capture_photo_is_older_than_5_minutes():
    filename = commands.get_last_photo_filename()
    return dom_utils.is_file_older_than_5_minutes(filename)


def measurement_is_older_than_5_minutes():
    row = denva_sensors_service.get_last_old_measurement()
    timestamp = row['timestamp']
    return dom_utils.is_timestamp_older_than_5_minutes(timestamp)


def healthcheck_test_runner():
    logger.info('Running healthcheck')
    now = datetime.now().time()
    if now < datetime.now().time().replace(hour=0, minute=15, second=0, microsecond=0):
        logger.info("TOO EARLY. Healthcheck skipped.")
        return

    if datetime.now().time().replace(hour=3, minute=0, second=0, microsecond=0) < now < datetime.now().time().replace(
            hour=3, minute=15, second=0, microsecond=0):
        logger.info("JUST AFTER RESTART. Healthcheck skipped.")
        return

    try:
        passed = healthcheck_test()

        if not passed:
            for i in range(1, attempts + 1):
                logger.warning(
                    "health check failed {} time(s) ... waiting {} seconds before retry".format(i, wait_time))
                time.sleep(wait_time)
                passed = healthcheck_test()

                if passed:
                    break

        if passed:
            logger.info("PASSED")
        else:
            logger.error("FAILED ( {} )".format(reasons))
            send_email_on_fail("A {} attempts to pass healthcheck failed due to {}".format(attempts, str(reasons)))
            commands.reboot("Health check failed")

    except Exception as e:
        logger.error("ERROR ( {} )".format(e), exc_info=True)
        send_email_on_fail(str(e))


def healthcheck_test() -> bool:
    is_ok = True

    # check is ui is running
    ip = 'http://' + commands.get_ip() + ':5000/hc'
    response = requests.get(ip)
    if response.status_code != requests.codes.ok:
        is_ok = False
        reasons.append("WEB APP is not working")

    # check is pictures are taken
    '''if capture_photo_is_older_than_5_minutes():
        is_ok = False
        reasons.append("Capture photo is not working")'''

    # check is app is running
    if measurement_is_older_than_5_minutes():
        is_ok = False
        reasons.append("Getting measurement is not working")

    if not is_ok:
        logger.warning("FAILED ( {} )".format(response))

    return is_ok


def send_email_on_fail(problem: str):
    email_sender_service.send_error_log_email("healthcheck", problem)


if __name__ == '__main__':
    try:
        config.set_mode_to('hc')
        data_files.setup_logging('hc')
        healthcheck_test_runner()
    except KeyboardInterrupt as keyboard_exception:
        print('Received request application to shut down.. goodbye. {}'.format(keyboard_exception))
        logging.info('Received request application to shut down.. goodbye!', exc_info=True)
    except BaseException as disaster:
        msg = 'Shit hit the fan and application died badly because {}'.format(disaster)
        print(msg)
        traceback.print_exc()
        logger.fatal(msg, exc_info=True)
