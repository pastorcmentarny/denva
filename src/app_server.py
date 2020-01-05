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
import email_sender_service
import commands

logger = logging.getLogger('app')

pictures = []

def main():
    counter = 0;
    while True:
        counter+=1
        time.sleep(5)
        last_picture = commands.capture_picture()

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
    end_time = timer()
    info('Setup took {} ms.'.format(int((end_time - start_time) * 1000)))


if __name__ == '__main__':
    print('Starting Server App ... \n Press Ctrl+C to shutdown')
    setup()
    try:
        main()
    except Exception as e:
        logger.error('Something went badly wrong\n{}'.format(e), exc_info=True)
        email_sender_service.send_error_log_email("application", "Application crashed due to {}.".format(e))

    sys.exit(0)
