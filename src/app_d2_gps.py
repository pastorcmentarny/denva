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
import sys
import logging
import time
from datetime import datetime
import config
import dom_utils
from common import data_files2

from gateways import local_data_gateway
from sensors import gps_sensor
from timeit import default_timer as timer

from services import gps_service

logger = logging.getLogger('app')
dom_utils.setup_logging('gps-sensor', True)
measurements_list = []
EMPTY = ''


def get_date_with_time_as_filename(name: str, file_type: str) -> str:
    dt = datetime.now()
    return f"{name}-{dt.year}-{dt.month:02d}-{dt.day:02d}.{file_type}"


def store_measurement(sensor_data: str, measurement: str):
    sensor_log_file = f"/home/ds/data/{get_date_with_time_as_filename(sensor_data, 'csv')}"
    try:
        with open(sensor_log_file, 'a+', newline=EMPTY, encoding='utf-8') as report_file:
            report_file.write(f'{measurement}\n')
    except IOError as exception:
        print(exception)
        # add flag to indicate that there is a problem


def application():
    global measurements_list
    measurement_counter = 0
    while True:
        measurement_counter += 1
        start_time = timer()
        result = gps_sensor.get_measurement()

        measurement_time = int((timer() - start_time) * 1000)  # in ms
        result.update({'counter': measurement_counter})
        result.update({'measurement_time': measurement_time})
        logger.info(gps_service.check_warning(result))

        data_files2.save_dict_data_to_file(result, 'gps-last-measurement')
        gps_service.check_warning(result)
        measurements_list.append(result)
        if len(measurements_list) > config.get_measurement_size():
            measurements_list.pop(0)

        if measurement_counter % 5 == 0:
            local_data_gateway.post_healthcheck_beat('denva2', 'gps')

        if measurement_counter % 100 == 0:
            data_files2.store_measurement('gps-data', measurements_list[-100:])

        if measurement_time > config.max_latency(fast=False):
            logger.warning("Measurement {} was slow.It took {} ms".format(measurement_counter, measurement_time))

        remaining_time_to_sleep = config.get_fast_refresh_rate() - (float((timer() - start_time)))
        if remaining_time_to_sleep > 0:
            time.sleep(remaining_time_to_sleep)


if __name__ == '__main__':
    try:
        application()
    except KeyboardInterrupt as keyboard_exception:
        print('Received request application to shut down.. goodbye. {}'.format(keyboard_exception))
        sys.exit(0)
    except Exception as exception:
        print(f'error:{exception}')
    except BaseException as disaster:
        msg = 'Shit hit the fan and application died badly because {}'.format(disaster)
        print(f'error:{disaster}')

    print('Application ended its life.')
