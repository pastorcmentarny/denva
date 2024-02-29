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

import logging.config

import sys
import time
import traceback
from datetime import datetime
from timeit import default_timer as timer

import smbus

import config

from common import data_files
from services import denva_measurement_service
from emails import email_sender_service
from gateways import local_data_gateway
from sensors import air_quality_sensor, two_led_service

bus = smbus.SMBus(1)

samples = []
pictures = []

logger = logging.getLogger('app')
warnings_logger = logging.getLogger('warnings')
config.set_mode_to('denva')
data_files.setup_logging(config.get_environment_log_path_for('denva_app'))
logger.info('Starting application ... \n Press Ctrl+C to shutdown')

app_startup_time = datetime.now()

counter = 1
led_status = 0


def main():
    measurement_counter = 0
    two_led_service.led_startup_show()
    while True:
        measurement_counter += 1
        logger.debug(f'Getting measurement no.{measurement_counter}')

        try:
            start_time = timer()
            measurement_time = denva_measurement_service.get_measurement_from_all_sensors(measurement_counter,
                                                                                          start_time)

            if measurement_counter % 2 == 0:
                local_data_gateway.post_healthcheck_beat('denva', 'app')

            remaining_of_five_s = 5 - (float(measurement_time) / 1000)

            if measurement_time > config.max_latency(fast=False):
                logger.warning(f'Measurement {measurement_counter} was slow.It took {measurement_time} ms')

            if remaining_of_five_s > 0:
                time.sleep(remaining_of_five_s)  # it should be 5 seconds between measurements
        except Exception as measurement_exception:
            logger.error(f'Measurement no. {measurement_counter} failed. Error: {measurement_exception}', exc_info=True)
            two_led_service.error_blink()


def cleanup_before_exit():
    two_led_service.on()
    sys.exit(0)


# TODO simplify logs in configs
if __name__ == '__main__':
    global points
    email_sender_service.send_ip_email('denva')
    try:
        logging.info("Sensor warming up, please wait...")
        air_quality_sensor.start_measurement()
        logging.info(f'Sensor needed {counter} seconds to warm up')
        two_led_service.off()
        main()
    except KeyboardInterrupt as keyboard_exception:
        print(f'Received request application to shut down.. goodbye. {keyboard_exception}')
        logging.info('Received request application to shut down.. goodbye!', exc_info=True)
        cleanup_before_exit()
        two_led_service.off()
    except Exception as exception:
        print(f'Whoops. {exception}')
        traceback.print_exc()
        logger.error(f'Something went badly wrong\n{exception}', exc_info=True)
        email_sender_service.send_error_log_email("application", f"Application crashed due to {exception}.")
        cleanup_before_exit()
    except BaseException as disaster:
        msg = f'Shit hit the fan and application died badly because {disaster}'
        print(msg)
        traceback.print_exc()
        logger.fatal(msg, exc_info=True)
        cleanup_before_exit()
