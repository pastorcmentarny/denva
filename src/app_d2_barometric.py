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
import traceback

import config
import logging
import sys
import time

import dom_utils
from common import loggy, data_files, data_writer
from gateways import local_data_gateway
from sensors import barometric_pressure_sensor

from timeit import default_timer as timer

from services import barometric_service

logger = logging.getLogger('app')
dom_utils.setup_logging('barometric-sensor', False)
measurements_list = []


def store_measurement(sensor_data: str, measurement: str):
    sensor_log_file = f"/home/ds/data/{dom_utils.get_today_date_with_time_as_filename(sensor_data, 'csv')}"
    try:
        with open(sensor_log_file, config.APPEND_WITH_READ_MODE, newline=config.EMPTY,
                  encoding=config.ENCODING) as report_file:
            report_file.write(f'{measurement}\n')
    except IOError as measurement_exception:
        print(measurement_exception)
        # add flag to indicate that there is a problem


def application():
    global measurements_list
    measurement_counter = 0
    while True:
        measurement_counter += 1

        start_time = timer()

        result = barometric_pressure_sensor.get_measurement()

        measurement_time = int((timer() - start_time) * 1000)  # in ms
        result.update({'counter': measurement_counter})
        result.update({'measurement_time': measurement_time})

        data_writer.save_dict_data_to_file(result, 'barometric-last-measurement')

        logger.info(barometric_service.get_warnings(result))
        dom_utils.update_measurement_list(measurements_list, result)

        if measurement_counter % 10 == 0:
            local_data_gateway.post_healthcheck_beat('denva2', 'barometric')

        data_files.store_last_100_measurement(measurement_counter, measurements_list, 'barometric-data')

        dom_utils.log_warning_if_measurement_slow(measurement_counter, measurement_time)

        remaining_time_to_sleep = config.get_normal_refresh_rate() - (float((timer() - start_time)))

        if remaining_time_to_sleep > 0:
            time.sleep(remaining_time_to_sleep)


if __name__ == '__main__':
    logger.info('Starting barometric app')
    try:
        application()
    except KeyboardInterrupt as keyboard_exception:
        msg = f'Received request application to shut down.. goodbye. {keyboard_exception}'
        loggy.log_with_print(msg)
        sys.exit(0)
    except Exception as exception:
        logger.fatal(exception, exc_info=True)
        print(f'error:{exception}')
        traceback.print_exc()
    except BaseException as disaster:
        msg = f'Shit hit the fan and application died badly because {disaster}'
        logger.fatal(msg, exc_info=True)
        print(f'Error:{msg}')
        traceback.print_exc()
    logger.warning('Application ended its life.')
