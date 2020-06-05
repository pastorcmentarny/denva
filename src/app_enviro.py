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
from timeit import default_timer as timer

import sys
import time

import config_service
from common import data_files, commands
from denva import cl_display
from gateways import local_data_gateway
from sensors import gas_service, humidity_bme_service, light_proximity_service
from sensors import particulate_matter_service
# from denviro import denviro_display //FIXME fix issue with font loading,but I don't use display now
from services import email_sender_service, sensor_warnings_service

logger = logging.getLogger('app')

message = ""
top_pos = 25
delay = 0.5  # Debounce the proximity tap
mode = 0  # The starting mode
last_page = 0
light = 1
values = {}
cycle = 0
on = True


def get_noise():
    # low, mid, high, amp = noise_service.get_noise_measurement()
    return ''  # low: {}, mid: {}, high: {}, amp: {}'.format(low, mid, high, amp)


def get_measurement() -> dict:
    p_1, p_2, p_10 = particulate_matter_service.get_measurement()
    measurement = {"temperature": humidity_bme_service.get_temperature(),  # unit = "C"
                   "pressure": humidity_bme_service.get_pressure(),  # unit = "hPa"
                   "humidity": humidity_bme_service.get_humidity(),  # unit = "%"
                   "light": light_proximity_service.get_illuminance(),  # unit = "Lux"
                   "proximity": light_proximity_service.get_proximity(),
                   "oxidised": gas_service.get_oxidising(),  # "oxidised"    unit = "kO"
                   "reduced": gas_service.get_reducing(),  # unit = "kO"
                   "nh3": gas_service.get_nh3(),  # unit = "kO"
                   "pm1": p_1,  # unit = "ug/m3"
                   "pm25": p_2,  # unit = "ug/m3"
                   "pm10": p_10}  # unit = "ug/m3"

    return measurement


def setup():
    logger.info("Starting up... Warming up sensors")
    start_time = timer()
    humidity_bme_service.warm_up()
    end_time = timer()
    logger.info('It took {} ms. Mounting drives...'.format(int((end_time - start_time) * 1000)))
    start_time = timer()
    commands.mount_all_drives('enviro')
    end_time = timer()
    logger.info('It took {} ms.'.format(int((end_time - start_time) * 1000)))


def main():
    measurement_counter = 0
    setup()
    while True:
        measurement_counter += 1
        logger.debug('Measurement No.{}'.format(measurement_counter))

        start_time = timer()
        measurement = get_measurement()
        # FIXME temporary disabled  denviro_display.display_on_screen(measurement)
        measurement['cpu_temp'] = commands.get_cpu_temp()
        end_time = timer()
        measurement_time = str(int((end_time - start_time) * 1000))  # in ms
        measurement['measurement_time'] = measurement_time
        logger.info('it took ' + str(measurement_time) + ' milliseconds to measure it.')
        cl_display.print_measurement(measurement)

        # FIXME do not work due to “sounddevice.PortAudioError: Error querying device -1" error
        # logger.warning(noise_service.get_noise_measurement())

        data_files.store_enviro_measurement(measurement)

        # deprecated but i will change settings to send them via config settings
        # measurement_storage_service.send('enviro', measurement)

        sensor_warnings_service.get_current_warnings_for_enviro()
        if measurement_counter % 2 == 0:
            local_data_gateway.post_healthcheck_beat('denviro', 'app')
        remaining_time_in_millis = 5 - (float(measurement_time) / 1000)

        if int(measurement_time) > config_service.max_latency(fast=False):
            logger.warning("Measurement {} was slow.It took {} ms".format(measurement_counter, measurement_time))

        if remaining_time_in_millis > 0:
            time.sleep(remaining_time_in_millis)


if __name__ == '__main__':
    config_service.set_mode_to('denviro')
    data_files.setup_logging('app')
    logger.info('Starting application ... \n Press Ctrl+C to shutdown')
    email_sender_service.send_ip_email('Denva Enviro+')

    try:
        commands.mount_all_drives()
        main()
    except KeyboardInterrupt as keyboard_exception:
        logger.error('Something went badly wrong\n{}'.format(keyboard_exception), exc_info=True)
        sys.exit(0)
