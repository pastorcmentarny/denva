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
import traceback
from datetime import datetime
from timeit import default_timer as timer

import sys

import config_service
import server.information_service as information
from common import app_timer, data_files, loggy
from gateways import local_data_gateway
from reports import report_service
from services import email_sender_service, metrics_service

logger = logging.getLogger('app')

pictures = []
email_cooldown = datetime.now()
report_generation_cooldown = datetime.now()


def should_send_email():
    global email_cooldown
    if app_timer.is_time_to_run_every_5_minutes(email_cooldown):
        logger.info('sending email..')
        report = report_service.create_for_current_measurements()
        email_sender_service.send(report, 'server')
        email_cooldown = datetime.now()


def main():
    global report_generation_cooldown
    counter = 0
    while True:
        counter += 1
        if counter % 2 == 0:
            local_data_gateway.post_healthcheck_beat('knyszogar', 'email')
        information.should_refresh()
        should_send_email()
        report_generation_cooldown = report_service.create_and_store_it_if_needed(report_generation_cooldown)


def setup():
    start_time = timer()
    config_service.set_mode_to('server')
    data_files.setup_logging('app')
    information.refresh_all()
    metrics_service.setup()
    loggy.log_time('Mothership App Setup', start_time, timer())


if __name__ == '__main__':
    print('Starting Server App ... \n Press Ctrl+C to shutdown')
    setup()
    try:
        main()
    except KeyboardInterrupt as keyboard_exception:
        print('Received request application to shut down.. goodbye. {}'.format(keyboard_exception))
        logging.info('Received request application to shut down.. goodbye!', exc_info=True)
    except Exception as exception:
        logger.error('Something went badly wrong\n{}'.format(exception), exc_info=True)
        email_sender_service.send_error_log_email("Mothership App", "Application crashed due to {}.".format(exception))
        sys.exit(1)
    except BaseException as disaster:
        msg = 'Shit hit the fan and application died badly because {}'.format(disaster)
        print(msg)
        traceback.print_exc()
        logger.fatal(msg, exc_info=True)
