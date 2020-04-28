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
import logging.config
import os
from datetime import datetime
from timeit import default_timer as timer

import smbus
import sys
import time
from PIL import ImageFont

import config_service
from common import data_files, commands, dom_utils
from denva import cl_display
# display removed from mothership import mini_display
from sensors import air_quality_service, environment_service, motion_service, two_led_service, uv_service
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


def get_pictures_path():
    pictures_path = []
    if len(pictures) > 2:
        pictures_path = [pictures[0], pictures[-1]]
    elif len(pictures) == 1:
        pictures_path = [pictures[0]]
    return pictures_path


def main():
    measurement_counter = 0
    two_led_service.led_startup_show()
    while True:
        try:
            measurement_counter += 1
            logger.debug('getting measurement no.{}'.format(measurement_counter))
            start_time = timer()
            data = get_data_from_measurement()
            data['cpu_temp'] = commands.get_cpu_temp()
            end_time = timer()

            measurement_time = str(int((end_time - start_time) * 1000))  # in ms
            data['measurement_counter'] = measurement_counter
            data['measurement_time'] = measurement_time
            data_files.store_measurement(data, motion_service.get_current_motion_difference())
            logger.debug('it took ' + str(measurement_time) + ' microseconds to measure it.')

            cl_display.print_measurement(data)

            data['picture_path'] = get_pictures_path()

            remaining_of_five_s = 5 - (float(measurement_time) / 1000)

            if remaining_of_five_s > 0:
                time.sleep(remaining_of_five_s)  # it should be 5 seconds between measurements

        except KeyboardInterrupt:
            logging.info('request application shut down.. goodbye!')
            cleanup_before_exit()


def cleanup_before_exit():
    two_led_service.on()
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
    except Exception as e:
        print('Whoops. '.format(e))
        logger.error('Something went badly wrong\n{}'.format(e), exc_info=True)
        email_sender_service.send_error_log_email("application", "Application crashed due to {}.".format(e))
        cleanup_before_exit()
