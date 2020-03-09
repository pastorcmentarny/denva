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
from timeit import default_timer as timer
import logging
import sys
import time
import data_files
from datetime import datetime

import app_timer
import local_data_gateway
import mothership.information_service as information
import webcam_utils

logger = logging.getLogger('server')

pictures = []
send_email_cooldown = datetime.now()

def should_send_email():
    global send_email_cooldown
    email_data = {}
    if app_timer.is_time_to_send_email(send_email_cooldown):
        email_data['information'] = information.get_information()
        email_data['denva'] = local_data_gateway.get_current_reading_for_denva()
        email_data['enviro'] = local_data_gateway.get_current_reading_for_enviro()
        send_email_cooldown = datetime.now()

def main():
    counter = 0
    while True:
        counter+=1
        time.sleep(5)
        last_picture = webcam_utils.capture_picture()
        information.should_refresh()
        if last_picture != "":
            pictures.append(last_picture)
            if len(pictures) > 5:
                pictures.pop(0)
        print(pictures)


def info(msg:str):
    logger.info(msg)
    print(msg)


def setup():
    start_time = timer()
    data_files.setup_logging('server')
    information.refresh_all()
    end_time = timer()
    info('Setup took {} ms.'.format(int((end_time - start_time) * 1000)))


if __name__ == '__main__':
    print('Starting Server App ... \n Press Ctrl+C to shutdown')
    setup()
    try:
        main()
    except Exception as e:
        logger.error('Something went badly wrong\n{}'.format(e), exc_info=True)
        #email_sender_service.send_error_log_email("application", "Application crashed due to {}.".format(e))

    sys.exit(0)
