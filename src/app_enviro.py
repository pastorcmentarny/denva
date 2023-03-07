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
from timeit import default_timer as timer

import config
from common import data_files, commands
from denva import cl_display
from denviro import denviro_sensors_service
from gateways import local_data_gateway
from sensors import gas_service, humidity_bme_service, light_proximity_service
from sensors import particulate_matter_service
from services import sensor_warnings_service

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
    oxidised, reduced, nh3 = gas_service.get_measurement()
    measurement = {config.FIELD_TEMPERATURE: humidity_bme_service.get_temperature(),  # unit = "C"
                   config.FIELD_PRESSURE: humidity_bme_service.get_pressure(),  # unit = "hPa"
                   config.FIELD_HUMIDITY: humidity_bme_service.get_humidity(),  # unit = "%"
                   config.FIELD_LIGHT: light_proximity_service.get_illuminance(),  # unit = "Lux"
                   config.FIELD_PROXIMITY: light_proximity_service.get_proximity(),
                   config.FIELD_OXIDISED: oxidised,  # config.FIELD_OXIDISED    unit = "kO"
                   config.FIELD_REDUCED: reduced,  # unit = "kO"
                   config.FIELD_NH3: nh3,  # unit = "kO"
                   config.FIELD_PM1: p_1,  # unit = "ug/m3"
                   config.FIELD_PM25: p_2,  # unit = "ug/m3"
                   config.FIELD_PM10: p_10}  # unit = "ug/m3"

    return measurement


def setup():
    logger.info("Starting up... Warming up sensors")
    start_time = timer()
    humidity_bme_service.warm_up()
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
        '''
        if config.is_cli_display():
            denviro_display.display_on_screen(measurement)
        '''
        measurement[config.FIELD_CPU_TEMP] = commands.get_cpu_temp()
        end_time = timer()
        measurement_time = str(int((end_time - start_time) * 1000))  # in ms
        measurement[config.FIELD_MEASUREMENT_TIME] = measurement_time
        local_data_gateway.post_denviro_measurement(measurement)
        logger.info('it took ' + str(measurement_time) + ' milliseconds to measure it.')
        cl_display.print_measurement(measurement)

        # FIXME do not work due to “sounddevice.PortAudioError: Error querying device -1" error
        # logger.warning(noise_service.get_noise_measurement())

        data_files.store_enviro_measurement(measurement, denviro_sensors_service.get_sensor_log_file())

        sensor_warnings_service.get_current_warnings_for_enviro()

        if measurement_counter % 2 == 0:
            local_data_gateway.post_healthcheck_beat('denviro', 'app')

        remaining_time_in_millis = 5 - (float(measurement_time) / 1000)

        if int(measurement_time) > config.max_latency(fast=False):
            logger.warning("Measurement {} was slow.It took {} ms".format(measurement_counter, measurement_time))

        if remaining_time_in_millis > 0:
            time.sleep(remaining_time_in_millis)


if __name__ == '__main__':
    config.set_mode_to('denviro')
    data_files.setup_logging('app')
    logger.info('Starting application ... \n Press Ctrl+C to shutdown')
    # TODO fix with send to server email_sender_service.send_ip_email('Denva Enviro+')

    try:
        main()
    except KeyboardInterrupt as keyboard_exception:
        print('Received request application to shut down.. goodbye. {}'.format(keyboard_exception))
        logging.info('Received request application to shut down.. goodbye!', exc_info=True)
        sys.exit(0)
    except Exception as exception:
        logger.error('Something went badly wrong\n{}'.format(exception), exc_info=True)
        # TODO fix with send to server email_sender_service.send_error_log_email('Denviro UI',
        #                                                  'Denviro UI crashes due to {}'.format(exception))
        sys.exit(1)
    except BaseException as disaster:
        msg = 'Shit hit the fan and application died badly because {}'.format(disaster)
        print(msg)
        traceback.print_exc()
        logger.fatal(msg, exc_info=True)
