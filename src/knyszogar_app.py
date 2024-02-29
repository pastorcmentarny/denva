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
from reports import report_service
from server import information_service as information
from common import loggy
from gateways import local_data_gateway, tube_client
from timeit import default_timer as timer

GENERATE_NOW = True

APP_NAME = 'server app'

logger = logging.getLogger('app')
dom_utils.setup_test_logging('app', False)
pictures = []
email_cooldown = datetime.now()
report_generation_cooldown = datetime.now()


def main():
    global report_generation_cooldown
    counter = 0
    local_data_gateway.post_device_on_off('knyszogar_app', True)
    report_service.create_and_store_it_if_needed(report_generation_cooldown, GENERATE_NOW)
    while True:
        logger.debug(f'Loop no. {counter}')
        start_time = timer()
        counter += 1

        local_data_gateway.post_healthcheck_beat('knyszogar', 'app')
        information.should_refresh(counter)

        tube_client.update()
        report_generation_cooldown = report_service.create_and_store_it_if_needed(report_generation_cooldown)
        end_time = timer()
        remaining = int((end_time - start_time) * 1000)
        sleep_time = (60000 - remaining) / 1000
        if sleep_time > 0:
            print(f'I will go sleep for {sleep_time} s')
            time.sleep(sleep_time)
        else:
            logger.warning(
                f'No sleep due to timer is below zero! Sleep time: {sleep_time}, counter {counter}, remaining {remaining}')


if __name__ == '__main__':
    loggy.log_with_print('Starting application')
    try:
        main()
    except KeyboardInterrupt as keyboard_exception:
        print(f'Received request application to shut down.. goodbye. {keyboard_exception}')
        logging.info('Received request application to shut down.. goodbye!', exc_info=True)

    except Exception as exception:
        logger.error(f'Something went badly wrong\n{exception}', exc_info=True)

        sys.exit(1)
    except BaseException as disaster:
        msg = f'Shit hit the fan and application died badly because {disaster}'
        print(msg)
        traceback.print_exc()
        logger.fatal(msg, exc_info=True)
