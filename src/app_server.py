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
from datetime import datetime
from timeit import default_timer as timer

import sys
import time

import config_service
import denvapa.information_service as information
from common import app_timer, data_files, loggy
from gateways import local_data_gateway
from denvapa import webcam_service
from reports import report_service
from services import email_sender_service

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
        time.sleep(5)
        if config_service.load_cfg()['mode'] == 'server' and config_service.is_cctv_camera_on():
            last_picture = webcam_service.capture_picture()
            if last_picture != "":
                pictures.append(last_picture)
                if len(pictures) > 5:
                    pictures.pop(0)
        if counter % 2 == 0:
            local_data_gateway.post_healthcheck_beat('server', 'app')
        information.should_refresh()
        should_send_email()
        report_generation_cooldown = report_service.create_and_store_it_if_needed(report_generation_cooldown)


def setup():
    start_time = timer()
    config_service.set_mode_to('server')
    data_files.setup_logging('app')
    information.refresh_all()
    loggy.log_time('Mothership App Setup', start_time, timer())


if __name__ == '__main__':
    print('Starting Server App ... \n Press Ctrl+C to shutdown')
    setup()
    try:
        main()
    except Exception as e:
        logger.error('Something went badly wrong\n{}'.format(e), exc_info=True)
        email_sender_service.send_error_log_email("Mothership App", "Application crashed due to {}.".format(e))
        sys.exit(1)
