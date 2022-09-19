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
import sys
import time
import traceback
from datetime import datetime

import dom_utils
# import server.information_service as information
from common import loggy
from gateways import local_data_gateway, tube_client
from timeit import default_timer as timer

"""
import config
from borg import webcam_service
from common import app_timer, data_files, loggy

from reports import report_service
from services import email_sender_service, metrics_service
"""
APP_NAME = 'server app'

logger = logging.getLogger('app')
dom_utils.setup_test_logging('app')
pictures = []
email_cooldown = datetime.now()
report_generation_cooldown = datetime.now()

"""
def should_send_email():
    global email_cooldown
    if app_timer.is_time_to_run_every_5_minutes(email_cooldown):
        logger.info('sending email..')
        report = report_service.create_for_current_measurements()
        email_sender_service.send(report, APP_NAME)
        email_cooldown = datetime.now()
"""


def main():
    global report_generation_cooldown
    counter = 0
    local_data_gateway.post_device_on_off('app', True)
    while True:
        logger.debug(f'Loop no. {counter}')
        start_time = timer()
        counter += 1

        if counter % 2 == 0:
            local_data_gateway.post_healthcheck_beat('knyszogar', 'app')
        # information.should_refresh()

        # every minute
        tube_client.update()
        # report_generation_cooldown = report_service.create_and_store_it_if_needed(report_generation_cooldown)
        end_time = timer()
        remaining = int((end_time - start_time) * 1000)
        counter += 1
        sleep_time = (60000 - remaining) / 1000
        print(f'I will go sleep for {sleep_time} s')
        time.sleep(sleep_time)


if __name__ == '__main__':
    loggy.log_with_print('Starting application')
    try:
        main()
    except KeyboardInterrupt as keyboard_exception:
        print('Received request application to shut down.. goodbye. {}'.format(keyboard_exception))
        logging.info('Received request application to shut down.. goodbye!', exc_info=True)
    except Exception as exception:
        logger.error('Something went badly wrong\n{}'.format(exception), exc_info=True)
        sys.exit(1)
    except BaseException as disaster:
        msg = 'Shit hit the fan and application died badly because {}'.format(disaster)
        print(msg)
        traceback.print_exc()
        logger.fatal(msg, exc_info=True)
