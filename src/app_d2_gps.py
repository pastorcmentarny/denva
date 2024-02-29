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
import config
import dom_utils
from common import data_files, data_writer

from gateways import local_data_gateway
from sensors import gps_sensor
from timeit import default_timer as timer

from services import gps_service

logger = logging.getLogger('app')
dom_utils.setup_logging('gps-sensor', False)
measurements_list = []


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
        logger.info(gps_service.get_warnings(result))

        data_writer.save_dict_data_to_file(result, 'gps-last-measurement')
        gps_service.get_warnings(result)
        dom_utils.update_measurement_list(measurements_list, result)

        if measurement_counter % 5 == 0:
            local_data_gateway.post_healthcheck_beat('denva2', 'gps')

        data_files.store_last_100_measurement(measurement_counter, measurements_list, 'gps-data')

        dom_utils.log_warning_if_measurement_slow(measurement_counter, measurement_time)

        remaining_time_to_sleep = config.get_fast_refresh_rate() - (float((timer() - start_time)))
        if remaining_time_to_sleep > 0:
            time.sleep(remaining_time_to_sleep)


if __name__ == '__main__':
    try:
        application()
    except KeyboardInterrupt as keyboard_exception:
        logger.warning(f'Received request application to shut down.. goodbye. {keyboard_exception}')
        sys.exit(0)
    except Exception as exception:
        logger.error(f'error:{exception}', exc_info=True)
    except BaseException as disaster:
        msg = f'Shit hit the fan and application died badly because {disaster}'
        logger.fatal(f'error:{disaster}', exc_info=True)

    logger.warning('Application ended its life.')
