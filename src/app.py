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
import logging.config
import os
import random
import sys
import time
import traceback
from datetime import datetime
from timeit import default_timer as timer

import smbus
from PIL import ImageFont

import config_service
from common import data_files, commands, dom_utils
from denva import cl_display
from gateways import local_data_gateway
from sensors import air_quality_service, environment_service, motion_service, two_led_service, uv_service, \
    led_matrix_service
from services import email_sender_service

bus = smbus.SMBus(1)

rr_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', 'Roboto-Regular.ttf'))
rr_12 = ImageFont.truetype(rr_path, 12)
rr_14 = ImageFont.truetype(rr_path, 14)

samples = []
pictures = []

logger = logging.getLogger('app')
warnings_logger = logging.getLogger('warnings')

app_startup_time = datetime.now()

counter = 1
led_status = 0


def get_data_from_measurement() -> dict:
    environment = environment_service.get_measurement()
    aqi = "n/a"
    eco2 = air_quality_service.get_eco2_measurement_as_string()
    tvoc = air_quality_service.get_tvoc_measurement_as_string()

    r, g, b = two_led_service.get_measurement()
    colour = dom_utils.to_hex(r, g, b)
    motion = motion_service.get_motion()
    two_led_service.warn_if_dom_shakes_his_legs(motion)

    uva_index, uvb_index, avg_uv_index = uv_service.get_measurements()

    return {
        "temp": environment['temp'],
        "pressure": environment['pressure'],
        "humidity": environment['humidity'],
        "gas_resistance": "{:.2f}".format(environment['gas_resistance']),
        "aqi": aqi,
        "colour": colour,
        "motion": motion,
        "uva_index": uva_index,
        "uvb_index": uvb_index,
        "r": r,
        "g": g,
        "b": b,
        "eco2": eco2,
        "tvoc": tvoc,
    }


def main():
    measurement_counter = 0
    two_led_service.led_startup_show()
    while True:
        measurement_counter += 1
        logger.debug('Getting measurement no.{}'.format(measurement_counter))
        start_time = timer()
        data = get_data_from_measurement()
        data['cpu_temp'] = commands.get_cpu_temp()
        end_time = timer()
        measurement_time = int((end_time - start_time) * 1000)  # in ms

        logger.info('Measurement no. {} took {} milliseconds to measure it.'
                    .format(measurement_counter, measurement_time))

        data['measurement_counter'] = measurement_counter
        data['measurement_time'] = str(measurement_time)
        data_files.store_measurement(data, motion_service.get_current_motion_difference())

        cl_display.print_measurement(data)

        if measurement_counter % 2 == 0:
            local_data_gateway.post_healthcheck_beat('denva', 'app')

        remaining_of_five_s = 5 - (float(measurement_time) / 1000)

        if measurement_time > config_service.max_latency(fast=False):
            logger.warning("Measurement {} was slow.It took {} ms".format(measurement_counter, measurement_time))

        if bool(random.getrandbits(1)):
            led_matrix_service.set_green()
        else:
            led_matrix_service.red()
        led_matrix_service.update_led_matrix()

        if remaining_of_five_s > 0:
            time.sleep(remaining_of_five_s)  # it should be 5 seconds between measurements


def cleanup_before_exit():
    two_led_service.on()
    led_matrix_service.set_red()
    sys.exit(0)


if __name__ == '__main__':
    global points
    config_service.set_mode_to('denva')
    data_files.setup_logging('app')
    logging.info('Starting application ... \n Press Ctrl+C to shutdown')
    email_sender_service.send_ip_email('denva')
    try:
        logging.info('Mounting network drives')
        commands.mount_all_drives()

        logging.info("Sensor warming up, please wait...")
        air_quality_service.start_measurement()
        motion_service.sample()
        logging.info('Sensor needed {} seconds to warm up'.format(counter))
        two_led_service.off()
        main()
    except KeyboardInterrupt as keyboard_exception:
        print('Received request application to shut down.. goodbye. {}'.format(keyboard_exception))
        logging.info('Received request application to shut down.. goodbye!', exc_info=True)
        cleanup_before_exit()
    except Exception as exception:
        print('Whoops. '.format(exception))
        logger.error('Something went badly wrong\n{}'.format(exception), exc_info=True)
        email_sender_service.send_error_log_email("application", "Application crashed due to {}.".format(exception))
        cleanup_before_exit()
    except BaseException as disaster:
        msg = 'Shit hit the fan and application died badly because {}'.format(disaster)
        print(msg)
        traceback.print_exc()
        logger.fatal(msg, exc_info=True)
