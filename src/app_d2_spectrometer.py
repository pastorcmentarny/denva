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
import dom_utils
from common import data_files, loggy, data_writer
from gateways import local_data_gateway
from sensors import spectrometer_sensor

logger = logging.getLogger('app')
dom_utils.setup_logging('spectrometer-sensor', False)
measurements_list = []


def application():
    global measurements_list
    measurement_counter = 0
    while True:
        measurement_counter += 1

        start_time = timer()

        result = spectrometer_sensor.get_measurement()

        measurement_time = int((timer() - start_time) * 1000)  # in ms
        result.update({'counter': measurement_counter})
        result.update({'measurement_time': measurement_time})

        data_writer.save_dict_data_to_file(result, 'spectrometer-last-measurement')

        dom_utils.update_measurement_list(measurements_list, result)

        if measurement_counter % 10 == 0:
            local_data_gateway.post_healthcheck_beat('denva2', 'spectrometer')

        data_files.store_last_100_measurement(measurement_counter, measurements_list, 'spectrometer-data')

        dom_utils.log_warning_if_measurement_slow(measurement_counter, measurement_time)

        remaining_time_to_sleep = config.get_fast_refresh_rate() - (float((timer() - start_time)))

        if remaining_time_to_sleep > 0:
            time.sleep(remaining_time_to_sleep)


if __name__ == '__main__':
    logger.info('Starting spectrometer app')
    try:
        application()
    except KeyboardInterrupt as keyboard_exception:
        msg = f'Received request application to shut down.. goodbye. {keyboard_exception}'
        loggy.log_with_print(msg, True)
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
