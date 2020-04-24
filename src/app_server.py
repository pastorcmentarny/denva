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
import mothership.information_service as information
from common import app_timer, data_files
from gateways import local_data_gateway
from mothership import app_server_service
from mothership import webcam_service
from services import information_service, email_sender_service

logger = logging.getLogger('app')

pictures = []
email_cooldown = datetime.now()
denva_report_email_cooldown = datetime.now()


# TODO fix it to ensure send report only once
def should_send_report_email():
    global denva_report_email_cooldown
    if app_timer.is_time_to_run_every_6_hours(denva_report_email_cooldown):
        logger.info('Preparing to send denva report email')
        start_time = timer()
        email_data = {'now': {
            'denva': local_data_gateway.get_current_reading_for_denva(),
            'enviro': local_data_gateway.get_current_reading_for_enviro()
        },
            'report': {
                'denva': local_data_gateway.get_yesterday_report_for_denva(),
                'enviro': local_data_gateway.get_yesterday_report_for_enviro(),
                'rickmansworth': information_service.get_data_about_rickmansworth(),
            }
        }
        end_time = timer()
        logger.info('It took {} ms to generate data'.format(int((end_time - start_time) * 1000)))
        email_sender_service.send(email_data, 'Report (via server)')
        denva_report_email_cooldown = datetime.now()


def should_send_email():
    global email_cooldown
    email_data = {}
    if app_timer.is_time_to_run_every_5_minutes(email_cooldown):
        logger.info('sending email..')
        email_data['information'] = information.get_information()
        email_data['denva'] = local_data_gateway.get_current_reading_for_denva()
        email_data['enviro'] = local_data_gateway.get_current_reading_for_enviro()
        email_data['warnings'] = local_data_gateway.get_current_warnings_for_all_services()
        email_data['logs'] = local_data_gateway.get_current_logs_for_all_services()
        email_data['system'] = app_server_service.get_current_system_information_for_all_services()
        email_sender_service.send(email_data, 'server')
        email_cooldown = datetime.now()


def main():
    counter = 0
    while True:
        counter += 1
        time.sleep(5)
        if config_service.load_cfg()['mode'] == 'server':
            last_picture = webcam_service.capture_picture()
            if last_picture != "":
                pictures.append(last_picture)
                if len(pictures) > 5:
                    pictures.pop(0)
        information.should_refresh()
        should_send_email()
        should_send_report_email()


def setup():
    start_time = timer()
    config_service.set_mode_to('server')
    data_files.setup_logging()
    information.refresh_all()
    end_time = timer()
    logger.info('Setup took {} ms.'.format(int((end_time - start_time) * 1000)))


if __name__ == '__main__':
    print('Starting Server App ... \n Press Ctrl+C to shutdown')
    setup()
    try:
        main()
    except Exception as e:
        logger.error('Something went badly wrong\n{}'.format(e), exc_info=True)
        email_sender_service.send_error_log_email("application", "Application crashed due to {}.".format(e))

    sys.exit(0)
